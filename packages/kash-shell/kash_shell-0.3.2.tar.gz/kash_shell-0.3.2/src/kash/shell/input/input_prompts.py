from InquirerPy.prompts.confirm import ConfirmPrompt
from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt
from prompt_toolkit.key_binding.key_processor import KeyPressEvent

from kash.config.text_styles import PROMPT_FORM
from kash.shell.input.inquirer_settings import configure_inquirer, custom_keybindings, custom_style

DEFAULT_INSTRUCTION = "Esc or Ctrl-C to cancel"


def input_simple_string(
    prompt_text: str,
    default: str = "",
    prompt_symbol: str = f"{PROMPT_FORM}",
    instruction: str = DEFAULT_INSTRUCTION,
) -> str | None:
    """
    Prompt user for a simple string.
    """
    configure_inquirer()
    prompt_text = prompt_text.strip()
    sep = "\n" if len(prompt_text) > 15 else " "
    prompt_message = f"{prompt_text}{sep}{prompt_symbol}"
    try:
        prompt = InputPrompt(
            message=prompt_message,
            default=default,
            long_instruction=f"({instruction})",
            style=custom_style,
            keybindings=custom_keybindings,
        )

        # Doing this more manually to try eager=True to avoid delay
        # when handling the escape key.
        @prompt.register_kb("escape", eager=True)
        def on_esc(event: KeyPressEvent) -> None:
            event.app.exit(result=None)

        response = prompt.execute()
    except EOFError:  # Handle Ctrl-D
        response = None
    return response


def input_confirm(
    prompt_text: str,
    default: bool = False,
    instruction: str = DEFAULT_INSTRUCTION,
) -> bool:
    """
    Prompt user for a yes/no answer.
    """
    configure_inquirer()
    prompt = ConfirmPrompt(
        message=prompt_text,
        default=default,
        long_instruction=f"({instruction})",
        style=custom_style,
        keybindings=custom_keybindings,
    )

    @prompt.register_kb("escape", eager=True)
    def on_escape(event: KeyPressEvent) -> None:
        event.app.exit(result=False)

    response = prompt.execute()
    return response


def input_choice(
    prompt_text: str,
    choices: list[str],
    default: str | None = None,
    mandatory: bool = False,
    instruction: str = DEFAULT_INSTRUCTION,
) -> str | None:
    """
    Prompt user to choose from a list of options.
    """
    configure_inquirer()
    prompt = ListPrompt(
        message=prompt_text,
        choices=choices,
        default=default,
        mandatory=mandatory,
        instruction=f"({instruction})",
        show_cursor=False,
        style=custom_style,
        keybindings=custom_keybindings,
    )

    # TODO: InquirerPy is missing kwargs for eager=True.
    @prompt.register_kb("escape")
    def on_escape(event: KeyPressEvent) -> None:
        event.app.exit()

    response = prompt.execute()
    return response
