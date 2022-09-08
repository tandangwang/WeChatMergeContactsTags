"""
copy (not move) all contacts from given tags to target tag (need to be created in advance)
1. will not delete previous tags
2. only keep one contact if duplicates exist
"""

import uiautomator2 as u2

# Global vars
d = u2.connect('you-device-serial') # you can get it by 'adb devices'
w, h = d.window_size()
# tags you want to get contacts from
tags_from = ['classmates', 'friends']
# tag you want to move contacts to
tag_to = 'recent-contacts'


def swipe_screen(finger_to='up'):
    """
    orientation the finger moves to
    :return:
    """
    fx = 0.5 * w
    tx = 0.5 * w
    fy = 0.9 * h
    ty = 0.2 * h

    if finger_to == 'up':
        d.swipe(fx, fy, tx, ty, duration=0.5)
    elif finger_to == 'down':
        d.swipe(tx, ty, fx, fy, duration=0.5)
    else:
        pass


def back_to_tag_homepage(go_to_top=False):
    while not d(text='通讯录标签').exists():
        d.press('back')
        d.sleep(0.5)
    d.sleep(1)

    if go_to_top:
        ele_search = d(text='搜索')
        while not ele_search.exists():
            swipe_screen('down')


def get_names_from_tags(the_tags, save_to_file='names.txt'):
    all_names = []

    for tag in the_tags:
        back_to_tag_homepage()
        ele_tag = d(text=tag)

        while not ele_tag.exists():
            swipe_screen('up')
            d.sleep(1)

        ele_tag.click()
        d(text='标签名字').wait()

        ele_name = d(resourceId='com.tencent.mm:id/iw8')

        while True:
            # handle one page
            for e_name in ele_name:
                name = e_name.get_text()
                if name in all_names:
                    continue
                all_names.append(name)

            if d(text='删除标签').exists():
                break
            swipe_screen('up')

    with open(save_to_file, 'w', encoding='utf-8') as f:
        lines = [name + '\n' for name in all_names]
        f.writelines(lines)

    return all_names


def add_persons(names):
    # whether the position is successfully obtained
    search_pos_obtained = False
    cx, cy = -1, -1

    ele_add = d(resourceId="com.tencent.mm:id/iwa", description="添加成员")

    ele_complete = d(textStartsWith='完成')

    for name in names:
        while not ele_add.exists():
            swipe_screen('up')
            d.sleep(0.5)

        ele_add.click()
        ele_complete.wait()

        if not search_pos_obtained:
            ele_input = d(text='搜索')
            cx, cy = ele_input.center()

        d.click(cx, cy)
        d.send_keys(name, clear=True)

        d(resourceId="com.tencent.mm:id/kpm", text=name).click()
        d.sleep(0.1)

        ele_complete.click()

    d(text='保存').wait()


if __name__ == '__main__':
    all_names = get_names_from_tags(tags_from, 'names.txt')

    back_to_tag_homepage(go_to_top=True)

    ele_target_tag = d(text=tag_to)
    while not ele_target_tag.exists():
        swipe_screen('up')
    ele_target_tag.click()
    d.sleep(1)

    all_names = list(dict.fromkeys(all_names))
    add_persons(all_names)

    d.sleep(2)
    d(text='保存').click()

    print('Done')
