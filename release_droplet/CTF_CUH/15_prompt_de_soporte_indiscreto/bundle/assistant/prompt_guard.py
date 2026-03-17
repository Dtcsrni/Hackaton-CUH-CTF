def build_prompt(system_prompt, context_blob, user_prompt):
    return system_prompt + '\n' + context_blob + '\n' + user_prompt
