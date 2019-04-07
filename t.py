shell_prompt = ""

while((shell_prompt = input('> ')).lower() != 'q'):
    print('you typed ' + shell_prompt)