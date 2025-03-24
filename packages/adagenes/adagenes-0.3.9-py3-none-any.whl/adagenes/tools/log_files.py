

def modify_content(file_content):
    # Split the content into lines
    lines = file_content.decode('utf-8').splitlines()

    # Process each line to strip everything after '::'
    #modified_lines = [line.split('::')[0] for line in lines]
    modified_lines = []
    for line in lines:
        newline = ''
        action = line.split('::')
        if len(action) > 1:
            newline += action[0]
        sort_filter_content = line.split(';;')
        if len(sort_filter_content) > 1:
            newline += "::" + sort_filter_content[1]

    # Join the modified lines back into a single string
    modified_content = '\n'.join(modified_lines).encode('utf-8')

    return modified_content
