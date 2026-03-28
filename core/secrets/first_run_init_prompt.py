from __future__ import annotations


def build_first_run_init_prompt(credential_name: str, purpose: str, config_paths: list[str]) -> str:
    path_lines = "\n".join([f"- {path}" for path in config_paths])
    return (
        f"当前无法继续，因为缺少必要凭证：{credential_name}\n\n"
        f"这个凭证的用途：{purpose}\n\n"
        f"建议配置位置：\n{path_lines}\n\n"
        f"配置完成后，请回复：已配置 {credential_name}\n"
        f"然后我会继续当前流程。"
    )
