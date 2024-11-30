import random
luckiest=[
'哇喵！你简直是幸运的化身喵！',
'你的运气真是好得让人羡慕喵~',
'今天的你，简直是万众瞩目的明星喵！',
'你一定有猫咪的护佑喵~',
'这种运气，真是让人想要一起庆祝喵！',
'来吧，快来分享你的快乐喵！',
'你是最幸运的，真是太棒了喵！',
'继续保持这种好运气喵~',
'你一定能赢得一切喵！',
'让我给你一个大大的喵~！'
]
very_lucky=[
'哇喵！你真是个幸运儿喵！',
'这种好运气真是让人心情大好喵~',
'继续这样下去，你会收获更多惊喜喵！',
'你真是个好运气的猫咪朋友喵！',
'这次投掷真是太棒了喵！',
'你的运气像阳光一样明媚喵~',
'让我们一起庆祝这份幸运喵！',
'你真是个幸运的家伙，继续加油喵！',
'这种感觉真好，像是在阳光下打滚喵~',
'你就是我的幸运星喵~！'
]
lucky=[
'嗯喵，虽然不是最幸运，但依然不错喵~',
'你的运气还不错，继续努力喵！',
'这次投掷让你有了小小的幸运喵~',
'有时候，幸运也会悄悄来临喵~',
'你在好运的路上，继续前行喵！',
'这次结果让人开心，继续保持喵~',
'你的运气像猫咪的胡须一样灵动喵~',
'不错喵，继续努力，下一次会更好喵！',
'你在幸运的轨道上，真棒喵~',
'让我们一起期待更好的结果喵~！'
]
normal=[
'嗯喵，这个结果有点平淡喵~',
'你就是个普通的猫咪，没关系喵~',
'有时候，平淡也是一种幸福喵~',
'这次投掷像是小猫咪的午睡一样安静喵~',
'不要气馁，下一次会更好喵！',
'有时候，普通也是一种幸运喵~',
'继续加油，期待更好的结果喵~',
'你的运气像我毛茸茸的尾巴一样柔软喵~',
'这只是个开始，未来会更精彩喵~',
'让我们一起期待下一次的惊喜喵~！'
]

unlucky=[
'哎呀喵，这次有点倒霉喵~',
'不过没关系，运气总会回来的喵！',
'这次投掷像是小猫咪的打盹，没什么特别喵~',
'你一定能翻身，继续努力喵！',
'有时候，倒霉也是生活的一部分喵~',
'别气馁，下一次会更好喵~',
'你的运气像是被猫咪的爪子抓了一下喵~',
'这只是个小插曲，未来会更精彩喵！',
'继续保持积极的心态，运气会转变喵~',
'让我们一起期待下一次的好运喵~！'
]

very_unlucky=[
'哎呀喵，这次真是有点倒霉喵~',
'不过别担心，运气总会改变的喵！',
'这种情况就像小猫咪掉进水里，没关系喵~',
'你一定能克服这些小挫折喵~',
'有时候，倒霉也是生活的调味品喵~',
'继续努力，下一次会更好喵！',
'你的运气像是被小狗狗追着跑，哈哈喵~',
'这只是暂时的，未来会更光明喵！',
'别放弃，继续追求你的好运喵~',
'让我们一起期待下一次的惊喜喵~！'
]
most_unlucky=[
'哎呀喵，这次真是最倒霉的结果喵~',
'不过别灰心，运气总会改变的喵！',
'这种情况就像小猫咪被雨淋湿，没关系喵~',
'你一定能从这次经历中变得更强喵~',
'有时候，最倒霉的结果也会带来意外的惊喜喵~',
'继续努力，下一次会更好喵！',
'你的运气像是被小狗狗追着跑，哈哈喵~',
'这只是暂时的，未来会更光明喵！',
'别放弃，继续追求你的好运喵~',
'让我们一起期待下一次的惊喜喵~！'
]

def return_joke(expect,limit):
    expect=expect[0]
    if expect == 1:
        temp = random.randint(0, len(luckiest)-1)
        return luckiest[temp]
    elif expect == 100:
        temp = random.randint(0, len(most_unlucky) - 1)
        return most_unlucky[temp]
    elif expect >=limit:
        temp = random.randint(0, len(very_unlucky) - 1)
        return very_unlucky[temp]
    elif expect*2==limit:
        temp = random.randint(0, len(normal) - 1)
        return normal[temp]
    elif expect*4<=limit:
        temp = random.randint(0, len(very_lucky) - 1)
        return very_lucky[temp]
    elif expect*2<limit:
        temp = random.randint(0, len(lucky) - 1)
        return lucky[temp]
    elif expect*4>=limit*3:
        temp = random.randint(0, len(very_unlucky) - 1)
        return very_unlucky[temp]
    else:
        temp = random.randint(0, len(unlucky) - 1)
        return unlucky[temp]
