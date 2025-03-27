from .grammar import SlackBlockGrammar, SlackInlineGrammar

class SlackBlockLexer:
    """
    Processes block-level elements while correctly tracking list depth.
    Uses the defined SlackBlockGrammar rules to parse Markdown structures into tokens.
    """
    GRAMMAR = SlackBlockGrammar

    def __init__(self):
        """
        Initialize the SlackBlockLexer with an empty token list and grammar rules.
        """
        self.tokens = []
        self.rules = self.GRAMMAR()

    def tokenize(self, text):
        """
        Tokenizes the input text into block-level Slack-compatible markdown.

        Args:
            text (str): The Markdown text to tokenize.

        Returns:
            list: A list of tokens representing the Markdown structure.
        """
        list_stack = []
        lines = text.split("\n")
        count = 0

        while count < len(lines):
            line = lines[count].rstrip()
            indent_level = len(line) - len(line.lstrip())

            # Adjust list stack based on current indent level
            while list_stack and list_stack[-1].get('indent', 0) >= indent_level:
                list_stack.pop()

            # Detect table by checking for "|"
            if line.startswith("|"):
                table_lines = [line]  # Start collecting table rows
                count += 1  # Move to next line

                while count < len(lines) and "|" in lines[count]:
                    table_lines.append(lines[count].rstrip())
                    count += 1  # Move to next line

                # Store the full table as a single token
                self.tokens.append({'type': 'TABLE', 'indent': indent_level, 'value': "\n".join(table_lines)})
                continue  # Skip normal processing since we already handled this block

            # Detect code block by checking for "```"
            elif line.startswith('```'):
                code_block_lines = [line]
                count += 1  # Move to next line

                while count < len(lines):
                    if lines[count].startswith('```'):
                        code_block_lines.append(lines[count].rstrip())
                        count += 1  # Move to next line
                        break  # End of code block
                    code_block_lines.append(lines[count].rstrip())
                    count += 1  # Move to next line

                # Store the full code block as a single token with raw content
                self.tokens.append({'type': 'CODE_BLOCK', 'indent': indent_level, 'value': "\n".join(code_block_lines), 'raw': True})
                continue  # Skip normal processing since we already handled this block

            # Regular Markdown processing
            for rule_name in [
                'SETEXT_HEADER', 'HEADER', 'HRULE', 'PARAGRAPH_BREAK',
                'BLOCK_QUOTE', 'CODE_BLOCK', 'UNORDERED_LIST', 
                'NUMBERED_LIST', 'LETTERED_LIST', 'PARAGRAPH'
            ]:
                pattern = getattr(self.rules, rule_name)
                match = pattern.match(line)
                if match:
                    token = self._create_token(rule_name, match, indent_level)
                    if token:
                        token.setdefault('indent', indent_level)
                        token.setdefault('value', line.strip())
                        self.tokens.append(token)
                        list_stack.append(token)
                    break
            else:
                # Default to paragraph token if no rule matches
                self.tokens.append({'type': 'PARAGRAPH', 'indent': indent_level, 'value': line.strip()})

            count += 1  # Move to next line

        return self.tokens

    def _create_token(self, rule_name, match, indent_level):
        """
        Creates a token based on the matched pattern.

        Args:
            rule_name (str): The name of the matching rule.
            match (re.Match): The regex match object.
            indent_level (int): The current indent level.

        Returns:
            dict: A dictionary representing the token.
        """
        token = {'type': rule_name, 'indent': indent_level, 'value': match.group(1).strip() if match.groups() else ""}

        if rule_name in ['HRULE', 'PARAGRAPH_BREAK']:
            return token
        elif rule_name == 'SETEXT_HEADER':
            token.update({'value': match.group(1).strip(), 'level': 1 if match.group(2).startswith('=') else 2})
        elif rule_name == 'TABLE':
            token['value'] = match.group(0).strip()
        elif rule_name == 'CODE_BLOCK':
            token['value'] = match.group(1)
        elif rule_name == 'BLOCK_QUOTE':
            token.update({'value': match.group(2), 'level': len(match.group(1).strip())})
        elif rule_name == 'HEADER':
            token.update({'value': match.group(2), 'level': len(match.group(1))})
        elif rule_name in ['UNORDERED_LIST', 'NUMBERED_LIST', 'LETTERED_LIST']:
            bullet = '-' if rule_name == 'UNORDERED_LIST' else f"{match.group(2)})"
            token.update({'value': match.group(3), 'bullet': bullet})
        else:
            token['value'] = match.group(1) if match.groups() else ""

        return token

class SlackInlineLexer:
    """
    Processes inline elements and converts them to Slack-compatible format.
    Uses the defined SlackInlineGrammar rules to transform inline Markdown elements.
    """
    GRAMMAR = SlackInlineGrammar
    
    def __init__(self):
        """
        Initializes the SlackInlineLexer with the default grammar rules.
        """
        self.rules = self.GRAMMAR()
    
    def parse(self, text):
        """
        Applies inline formatting to the given text.
        
        Uses the grammar rules defined in SlackInlineGrammar to match inline elements 
        and replace them with Slack-compatible formatting.
        
        Args:
            text (str): The text to apply inline formatting to.
        
        Returns:
            str: The text with inline formatting applied.
        """
        def replace_italic(match):
            return f"_{match.group(1) or match.group(2)}_"
        
        def user_mention(match):
            if match.group(1).startswith('<@'):
                return match.group(1)  # Return already formatted Slack mention
            return f"<{match.group(1)}>"  # Format @username into Slack format
        
        def channel_mention(match):
            if match.group(1).startswith('<#'):
                return match.group(1)  # Return already formatted Slack channel mention
            return f"<{match.group(1)}>"  # Format #channel_name into Slack format
        
        text = self.rules.ITALIC.sub(replace_italic, text)
        text = self.rules.BOLD_ITALIC.sub(r'*_\2_*', text)
        text = self.rules.BOLD.sub(r'*\2*', text)
        text = self.rules.STRIKETHROUGH.sub(r'~\1~', text)
        text = self.rules.IMAGE.sub(r'<\2|\1>', text)
        text = self.rules.LINK.sub(r'<\2|\1>', text)
        text = self.rules.INLINE_CODE.sub(r'`\1`', text)
        text = self.rules.LINEBREAK.sub(r'\n', text)
        text = self.rules.MENTION_USER.sub(user_mention, text)
        text = self.rules.MENTION_CHANNEL.sub(channel_mention, text)
        
        return text
