import IPython.terminal.prompts
from IPython.terminal.prompts import Token

class CustomPrompt( IPython.terminal.prompts.Prompts ):
    @classmethod
    def setProfile( cls, profile ):
        cls.profile = profile

    def in_prompt_tokens(self, cli=None):
       return [
            (Token.Prompt, 'aws[{}] '.format( self.profile ) ),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, ': '),
            ]

    def out_prompt_tokens(self):
       return [
            (Token.OutPrompt, 'out '),
            (Token.OutPromptNum, str(self.shell.execution_count)),
            (Token.OutPrompt, ': '),
        ]

import traitlets.config.loader
config = traitlets.config.loader.Config()
config.TerminalInteractiveShell.prompts_class=CustomPrompt
