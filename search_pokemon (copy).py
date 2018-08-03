import pathlib
from gzuro import Grid, SelectList, Text, TextInput, Image


def info_pokedex_number(number):
    data_info = ""
    with open('inform_pokemon/{}'.format(str(number).zfill(3))) as f:
        line = f.read().split('\n')
        data_info += line[0] + "\n"
        data_info += "Height: " + line[5][6:] + "\n"
        data_info += "Weight: " + line[6][6:] + "\n"
        data_info += "Category: " + line[10] + "\n"
        data_info += "Abilities: " + line[8][8:] + "\n"
        data_info += "Type: " + line[11][4:] + "\n"
    return data_info

data = []
for i in range(1, 152):
    with open('inform_pokemon/{}'.format(str(i).zfill(3))) as f:
        data.append(f.readline().rstrip())
data_dir = dict(zip(data, range(1, 152)))


def data_name():
    data_namelist = []
    for i in range(1, 152):
        with open('inform_pokemon/{}'.format(str(i).zfill(3))) as f:
            data_namelist.append(f.readline().rstrip())
    return data_namelist


def search_name(string):
    list = data_name()
    name = []
    for i in list:
        if i.lower().startswith(string.lower()):
            name.append(i)
    return name

root = Grid(cols=2)
root_left = Grid(rows=2)
root_right = Grid(cols=2)

current_dir = pathlib.Path(__file__).parent
image_path = 'image_pokemon/001.png'
root_right.append(Image(str(image_path)))

text2 = Text(info_pokedex_number(1))
root_right.append(text2)


text_input = TextInput()
select_list = SelectList(choices=data_name(), default=data_name()[0])


@text_input.on_change
def change_text():
    if text_input.content != "":
        name = text_input.content
        a = search_name(name)
        select_list.choices = a
        select_list.default = a
    else:
        select_list.choices = ""
        select_list.default = ""


@select_list.on_selection
def change_text():
    global text2
    global root_right
    root_right.delete()

    text2.content = select_list.selected
    text2.content[0].upper()
    stt = data_dir[text2.content]
    stt = str(stt).zfill(3)

    current_dir = pathlib.Path(__file__).parent
    image_path = current_dir / 'image_pokemon/{}.png'.format(stt)

    root_right = Grid(cols=2)
    text2 = Text(info_pokedex_number(stt))
    root_right.append(Image(str(image_path)))
    root_right.append(text2)
    root.append(root_right)


root.append(root_left)
root.append(root_right)
root_left.append(text_input)
root_left.append(select_list)
root.run()
