import os
import subprocess
import sys
import tempfile

import click
import ruamel.yaml
from jinja2 import Template
from loguru import logger
from pydantic_core import to_jsonable_python

import api_sos as sos
from api_sos import CheckResult
from entity import APICheck, Input
from generate import file_add_checks, openapi_to_checks
from utils import auto_reader, coro

VERSION = "1.0.0"


def setup_logger(verbose: bool = False):
    """Setup logger with appropriate level based on verbose flag"""
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "INFO", backtrace=True, diagnose=True)


@click.group()
def api_sos():
    """API SOS - API testing tool"""
    pass


async def interactive_edit_check(input_file: str, check: APICheck, result: CheckResult, index: int):
    """
    交互式编辑指定的检查项

    :param input_file: 输入文件路径
    :param check: 需要编辑的检查项
    :param result: 检查结果
    :param index: 检查项在列表中的索引
    """
    if not result.diffs or not result.response:
        return

    # 获取环境变量中的编辑器，默认为vim
    editor = os.environ.get("EDITOR", "vim")

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+", delete=False) as temp_file:
        # 获取当前断言内容
        current_assert = check.assert_

        # 如果没有断言，创建一个空断言
        if current_assert is None:
            from entity import AssertResponse

            current_assert = AssertResponse(
                headers=None, http_status=None, http_version=None, encoding="utf-8", content=None
            )

        # 创建包含当前断言和实际响应的YAML内容
        yaml_content = {
            "assert": to_jsonable_python(current_assert),
            "actual": to_jsonable_python(result.response),
            "name": check.name,
        }

        # 将内容写入临时文件
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        yaml.dump(yaml_content, temp_file)
        temp_file_path = temp_file.name

        try:
            # 打开编辑器编辑临时文件
            logger.info(f"正在打开编辑器编辑检查项 '{check.name}'...")
            subprocess.run([editor, temp_file_path], check=True)

            # 读取编辑后的文件内容
            edited_content = auto_reader(temp_file_path)
            if "actual" in edited_content:
                del edited_content["actual"]

            if "name" in edited_content:
                del edited_content["name"]

            # 更新检查项的断言
            if "assert" in edited_content:
                check.assert_ = edited_content["assert"]

                # 读取原始输入文件
                input_data = auto_reader(input_file)

                # 确保索引有效
                if index < len(input_data["checks"]):
                    # 只更新断言部分
                    input_data["checks"][index]["assert"] = edited_content["assert"]

                    # 写回文件
                    with open(input_file, "w") as f:
                        yaml = ruamel.yaml.YAML()
                        yaml.preserve_quotes = True
                        yaml.dump(input_data, f)

                    logger.info(f"已更新检查项 '{check.name}' 的断言")
                else:
                    logger.error(f"无法更新检查项，索引 {index} 超出范围")
        except Exception as e:
            logger.error(f"编辑检查项时出错: {e}")
        finally:
            # 删除临时文件
            os.unlink(temp_file_path)


@click.command()
@click.option("-v", "--verbose", is_flag=True, show_default=True, default=False, help="Enable debug mode")
@click.option("--concurrent", default=1, help="Run the script concurrently")
@click.option(
    "-i",
    "--interactive",
    default=False,
    is_flag=True,
    show_default=True,
    help="Run the script, if the result is different to aspected, interactively edit the input file",
)
@click.option(
    "--endpoint",
    default=None,
    help="The endpoint to be used, if not provided, the endpoint given in input will be used",
)
@click.option(
    "--variables",
    default=None,
    help="The file to be used as variables, should be a json or yaml. if provided, all value will replaced in input",
)
@click.argument("file_input")
@logger.catch(reraise=True, onerror=lambda _: sys.exit(1))
@coro
async def run(
    verbose: bool, file_input: str, concurrent: int, interactive: bool, endpoint: str | None, variables: str | None
):
    setup_logger(verbose)
    assert isinstance(interactive, bool), "interactive_edit must be a boolean, please input True or False"

    # Load variables if provided
    variables_dict = None
    if variables:
        logger.debug(f"loading variables from {variables}")
        variables_dict = auto_reader(variables)

    logger.debug(f"loading input {file_input}")
    input_ = Input.load(file_input)

    assert input_.version == VERSION

    input_.endpoint = endpoint or input_.endpoint

    logger.info(f"Running the input {file_input} with {concurrent} concurrent processes")

    results = await sos.run(input_, concurrent, variables_dict)

    # 处理结果
    has_error = False
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            has_error = True
            logger.error(str(result))
        elif isinstance(result, CheckResult):
            if result.error:
                has_error = True
                logger.error(str(result))
            elif result.diffs:
                logger.warning(str(result))
                # 如果启用了交互式模式且存在差异，进入交互式编辑
                if interactive and result.diffs:
                    await interactive_edit_check(file_input, input_.checks[i], result, i)
            else:
                logger.success(str(result))

    if has_error or any(isinstance(r, CheckResult) and r.diffs for r in results):
        sys.exit(1)
    else:
        logger.success("All tests passed!")


@click.command()
@click.option("-v", "--verbose", is_flag=True, show_default=True, default=False, help="Enable debug mode")
@click.argument("schema")
@click.option(
    "--key", default=None, help="The key to be used in the schema, if given, only the key in schema will be generated"
)
@click.argument("output")
@click.option(
    "--endpoint",
    default=None,
    help="The endpoint to be used for recording responses, required when --no-record is not set",
)
@click.option(
    "--concurrent",
    default=1,
    help="Number of concurrent requests when recording responses",
)
@click.option(
    "--headers",
    default=None,
    help="Headers to be used for requests, should be a json or yaml file",
)
@click.option(
    "--headers-variables",
    default=None,
    help="Variables to be used in headers template, should be a json or yaml file",
)
@click.option(
    "--no-record/-nr",
    is_flag=True,
    show_default=True,
    default=False,
    help="If try to request the endpoint and record the response as assert",
)
@click.option(
    "--no-example/-ne",
    is_flag=True,
    show_default=True,
    default=False,
    help="If try to generate checks from example in schema",
)
@logger.catch(reraise=True, onerror=lambda _: sys.exit(1))
@coro
async def generate(
    verbose: bool,
    schema: str,
    output: str,
    key: str | None = None,
    endpoint: str | None = None,
    concurrent: int = 1,
    headers: str | None = None,
    headers_variables: str | None = None,
    no_example: bool = False,
    no_record: bool = False,
):
    setup_logger(verbose)
    logger.debug(f"generating input {schema}")
    checks = openapi_to_checks(schema, key=key, from_example=not no_example)

    # 处理 headers
    headers_dict = None
    if headers:
        logger.debug(f"loading headers from {headers}")
        headers_dict = auto_reader(headers)
        if headers_variables:
            logger.debug(f"loading headers variables from {headers_variables}")
            variables_dict = auto_reader(headers_variables)
            # 使用 variables_dict 处理 headers_dict 中的模板
            rendered_headers = {}
            for key, value in headers_dict.items():
                if isinstance(value, str) and "{{" in value and "}}" in value:
                    template = Template(value)
                    rendered_headers[key] = template.render(**variables_dict)
                else:
                    rendered_headers[key] = value
            headers_dict = rendered_headers

    if not no_record:
        if endpoint is None:
            raise click.UsageError(
                "\nEndpoint is required when recording responses (--no-record is not set).\n"
                "Please either:\n"
                "1. Provide an endpoint using --endpoint option\n"
                "   Example: api-sos generate openapi.yaml output.yaml --endpoint http://localhost:8000\n"
                "2. Or use --no-record to skip response recording\n"
                "   Example: api-sos generate openapi.yaml output.yaml --no-record"
            )

        # 尝试运行生成的检查并记录响应
        logger.info("Running generated checks to record responses...")
        input_ = Input(version=VERSION, endpoint=endpoint, checks=checks)

        # 如果提供了 headers，应用到所有检查
        if headers_dict:
            for check in checks:
                check.headers = headers_dict

        # 运行检查并获取响应
        results = await sos.run(input_, concurrent=concurrent)

        # 更新检查的断言
        for check, result in zip(checks, results):
            if not isinstance(result, Exception) and result.response:
                check.assert_ = result.response

    # 如果提供了 headers，恢复到原始模板形式
    if headers:
        original_headers = auto_reader(headers)
        for check in checks:
            check.headers = original_headers

    file_add_checks(output, checks)


api_sos.add_command(run)
api_sos.add_command(generate)

if __name__ == "__main__":
    api_sos()
