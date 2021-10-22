import json

from discord import File
from datetime import datetime, timedelta
from easy_pil import Editor, Canvas, load_image_async, Font

level = ['Level-5+', 'Level-10+', 'Level-15+', 'Level-20+', 'Level-25+', 'Level-30+', 'Level-40+', 'Level-50+', 'Level-75+', 'Level-100+', 'Level-150+']
levelnum = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150]

class Levels():
  def increase_xp(userid: str, guildid: str, increaseby: int):
    with open("jsons/levels.json", "r") as f:
      data = json.load(f)
    try:
      if data[guildid] is not None:
        try:
          if data[guildid][userid] is not None:
            xp = data[guildid][userid]['xp']
            data[guildid][userid]['xp'] = (increaseby+xp)
            new_level = int((xp+increaseby)/100)
            
            lvl = data[guildid][userid]['level']
            send_data = "NONE"

            if new_level > lvl:
              data[guildid][userid]['level'] = new_level
              data[guildid][userid]['xp'] = 0
              for i in range(len(level)):
                if new_level == levelnum[i]:
                  send_data = f"NEW-LEVEL-ROLES {new_level} {level[i]}"
                  break
                else:
                  send_data = f"NEW-LEVEL {new_level}"

            with open('jsons/levels.json', "w") as f:
              json.dump(data, f)

            return send_data
        except:
          data[str(guildid)][str(userid)] = {}
          data[str(guildid)][str(userid)]['xp'] = 0
          data[str(guildid)][str(userid)]['level'] = 1
          data[str(guildid)][str(userid)]['card'] = 0
          data[str(guildid)][str(userid)]['text'] = "#fff"
          data[str(guildid)][str(userid)]['bar'] = "#17F3F6"
          data[str(guildid)][str(userid)]['blend'] = 0
          with open("jsons/levels.json", "w") as f:
            json.dump(data, f)
    except:
      data[str(guildid)] = {}
      data[str(guildid)][str(userid)] = {}
      data[str(guildid)][str(userid)]['xp'] = 0
      data[str(guildid)][str(userid)]['level'] = 1
      data[str(guildid)][str(userid)]['card'] = 0
      data[str(guildid)][str(userid)]['text'] = "#fff"
      data[str(guildid)][str(userid)]['bar'] = "#17F3F6"
      data[str(guildid)][str(userid)]['blend'] = 0
      with open("jsons/levels.json", "w") as f:
        json.dump(data, f)
    return "NONE"

  def decrease_xp(userid: str, guildid: str, mode: str, decreaseby: int):
    with open("jsons/levels.json", "r") as f:
      data = json.load(f)
    data[guildid][userid][mode] =- decreaseby
    with open("jsons/levels.json", "w") as f:
      json.dump(data, f)
  
  def get_user_details(guildid: str, userid: str):
    with open("jsons/levels.json", "r") as f:
      data = json.load(f)
    try:
      user = data[guildid][userid]
      return user
    except:
      return None

  async def make_user_rank_card(guildid: str, userid: str, avatarurl: str, username: str):
      with open('jsons/levels.json', "r") as f:
        data = json.load(f)
      xp = data[str(guildid)][str(userid)]['xp']
      lvl = data[str(guildid)][str(userid)]['level']
      image = data[str(guildid)][str(userid)]['card']

      next_level_xp = (lvl+1) * 100
      current_level_xp = lvl * 100
      xp_need = next_level_xp
      xp_have = data[str(guildid)][str(userid)]['xp']

      percentage = int(((xp_have * 100)/ xp_need))

      if percentage < 1:
        percentage = 0
      
      ## Rank card
      background = Editor(f"images/{image}.png")
      profile = await load_image_async(str(avatarurl))

      profile = Editor(profile).resize((150, 150)).circle_image()

      poppins = Font().poppins(size=40)
      poppins_small = Font().poppins(size=30)

      co = (0, 0, 0)
      TRANSPARENCY = 25  # Degree of transparency, 0-100%
      OPACITY = int(255 * TRANSPARENCY)
      ima = Editor("images/anothertry.png")
      
      if data[str(guildid)][str(userid)]['blend'] == 1:
        background.blend(image=ima, alpha=.5, on_top=False)

      #background.paste(square.image, (600, -250))
      background.paste(profile.image, (30, 30))

      background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
      background.bar(
          (30, 220),
          max_width=650,
          height=40,
          percentage=percentage,
          fill=data[str(guildid)][str(userid)]['bar'],
          radius=20,
      )
      background.text((200, 40), str(username), font=poppins, color=data[str(guildid)][str(userid)]['text'])

      background.rectangle((200, 100), width=350, height=2, fill=data[str(guildid)][str(userid)]['bar'])
      background.text(
          (200, 130),
          f"Level : {lvl}   "
          + f" XP : {xp} / {(lvl+1) * 100}",
          font=poppins_small,
          color=data[str(guildid)][str(userid)]['text'],
      )

      file = File(fp=background.image_bytes, filename="images/card.png")
      return file

class Economy():
  def increase_money(userid: str):
    with open("jsons/mainBank.json", "r") as f:
      data = json.load(f)
    try:
      if data[str(userid)] is not None:
        if data[str(userid)]['sb'] == 1:
          data[str(userid)]['bank'] += 2000
        else:
          data[str(userid)]['bank'] += 1000
        
        with open("jsons/mainBank.json", "w") as f:
          json.dump(data, f)
    except:
      data[str(userid)] = {}
      data[str(userid)]['wallet'] = 0
      data[str(userid)]['bank'] = 100
      data[str(userid)]['hide'] = 0
      data[str(userid)]['sb'] = 0

  def get_bank_data():
    with open("jsons/mainBank.json", "r") as f:
      data = json.load(f)
    return data

  def update_bank(user, change = 0, mode="wallet"):
    users = Economy.get_bank_data()

    users[str(user.id)][mode] +=change

    with open("jsons/mainBank.json", "w") as f:
      json.dump(users, f)
    
    bal = [users[str(user.id)]['wallet'],users[str(user.id)]['bank']]

    return bal

  def open_account(user): 
    users = Economy.get_bank_data()
    
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)] = {}
      users[str(user.id)]['wallet'] = 0
      users[str(user.id)]['bank'] = 100
      users[str(user.id)]['hide'] = 0
      users[str(user.id)]['sb'] = 0

    with open("jsons/mainBank.json", "w") as f:
      json.dump(users, f)
    
    return True
  
  def decrease_money(userid: str, decreaseby: int):
    with open("jsons/mainBank.json", "r") as f:
      users = json.load(f)
    users[str(userid)]['bank'] -= decreaseby
    with open("jsons/mainBank.json", "w") as f:
      json.dump(users, f)

class General():
  async def make_welcome_card(member):
    pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)
    if pos == 1:
      te = "st"
    elif pos == 2:
      te = "nd"
    elif pos == 3:
      te = "rd"
    else:
      te = "th"

    background = Editor("jsons/wlcbg.jpg")
    profile_image = await load_image_async(str(member.avatar_url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font().poppins(size=50, variant="bold")

    poppins_small = Font().poppins(size=25, variant="regular")
    poppins_light = Font().poppins(size=20, variant="light")

    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline="gold", stroke_width=4)

    #guildname = member.guild.name
    background.text((400, 260), "WELCOME TO KINGDOM", color="white", font=poppins, align="center")

    background.text(
        (400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center"
    )

    background.text(
        (400, 360),
        f"You are the {pos}{te} Member",
        color="#0BE7F5",
        font=poppins_small,
        align="center",
    )

    file = File(fp=background.image_bytes, filename="jsons/wlcbg.jpg")
    return file

  def add_user_data(user):
    def add_levels():
      with open("jsons/levels.json", "r") as f:
        data = json.load(f)
      if str(user.id) in data[str(user.guild.id)]:
        return
      data[str(user.guild.id)][str(user.id)] = {}
      data[str(user.guild.id)][str(user.id)]['xp'] = 0
      data[str(user.guild.id)][str(user.id)]['level'] = 1
      data[str(user.guild.id)][str(user.id)]['card'] = 0
      data[str(user.guild.id)][str(user.id)]['text'] = "#fff"
      data[str(user.guild.id)][str(user.id)]['bar'] = "#17F3F6"
      data[str(user.guild.id)][str(user.id)]['blend'] = 0
    
    def add_mute_data():
      with open("jsons/muted.json", "r") as f:
        data2 = json.load(f)
      if data2 is not None:
        try:
          if str(user.id) in data2[str(user.guild.id)]:
            return
          data2[str(user.guild.id)][str(user.id)]['muted'] = 0
          data2[str(user.guild.id)][str(user.id)]['muted_on'] = 0
          data2[str(user.guild.id)][str(user.id)]['unmute_at'] = 0

          with open("jsons/muted.json", "w") as f:
            json.dump(data2, f)
        except:
          pass
      
    
    def open_account():
      Economy.open_account(user)

    add_levels()
    open_account()
    add_mute_data()

  def remove_user_data(user):
    def delete_levels():
      with open("jsons/levels.json", "r") as f:
        data1 = json.load(f)
      del data1[str(user.guild.id)][str(user.id)]
      with open("jsons/levels.json", "w") as f:
        json.dump(data1, f)
      
    def delete_account():
      with open("jsons/mainBank.json", "r") as f:
        data2 = json.load(f)
      del data2[str(user.id)]
      with open("jsons/mainBank.json", "w") as f:
        json.dump(data2, f)

    def delete_mute_data():
      with open("jsons/muted.json", "r") as f:
        data3 = json.load(f)
      del data3[str(user.guild.id)][str(user.id)]
      with open("jsons/muted.json", "r") as f:
        json.dump(data3, f)

    delete_levels()
    delete_account()
    delete_mute_data()

class Auto_Moderation():
  def mute(guildid: str, userid: str, curtime: str, unmuteafter: int):
    with open("jsons/muted.json", "r") as f:
      data = json.load(f)
    unmute_at = Time.add_time(curtime, unmuteafter)
    try:
      if data[str(guildid)] is not None:
        try:
          if data[str(guildid)][str(userid)] is not None:
            if data[str(guildid)][str(userid)]['muted'] == 0:
              data[str(guildid)][str(userid)]['muted'] = 1
              data[str(guildid)][str(userid)]['muted_on'] = curtime
              data[str(guildid)][str(userid)]['unmute_at'] = unmute_at

              with open("jsons/muted.json", "w") as f:
                json.dump(data, f)

              return "DONE"
            else:
              return "ALREADY_MUTED"
        except:
          data[str(guildid)][str(userid)] = {}
          data[str(guildid)][str(userid)]['muted'] = 1
          data[str(guildid)][str(userid)]['muted_on'] = curtime
          data[str(guildid)][str(userid)]['unmute_at'] = unmute_at
          with open("jsons/muted.json", "w") as f:
            json.dump(data, f)
          return "DONE"
    except:
      data[str(guildid)] = {}
      data[str(guildid)][str(userid)] = {}
      data[str(guildid)][str(userid)]['muted'] = 1
      data[str(guildid)][str(userid)]['muted_on'] = curtime
      data[str(guildid)][str(userid)]['unmute_at'] = unmute_at
      with open("jsons/muted.json", "w") as f:
        json.dump(data, f)
      return "DONE"


class Time():
  def convert_time(num: int, mode: str):
    if mode == "s":
      return num
    elif mode == "m":
      return num*60
    elif mode == "hr":
      return num*60*60
    else:
      return None

  def get_current_time(mode: str):
    if mode == "NORMAL":
      return datetime.utcnow()
    elif mode == "DATE":
      return datetime.utcnow().strftime("%d")
    elif mode == "HOUR":
      return datetime.utcnow().strftime("%H")
    elif mode == "MIN":
      return datetime.utcnow().strftime("%M")
    elif mode == "DHM":
      date = datetime.utcnow().strftime("%d")
      hour = datetime.utcnow().strftime("%H")
      min = datetime.utcnow().strftime("%M")
      min = datetime.utcnow().strftime("%M")
      data = date, " ", hour, " ", min
      return data

  def add_time(now: str, addTime: int):
    new_time = now+timedelta(seconds=addTime)
    return new_time


#date = datetime.utcnow().strftime("%d")
#hour = datetime.utcnow().strftime("%H")
#min = datetime.utcnow().strftime("%M")