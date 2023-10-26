from player import Player
import xml.etree.ElementTree as et

class PlayerFactory:

    def to_json(self, players):
        return[{
            "nickname": player.nickname,
            "email": player.email,
            "date_of_birth": f"{player.date_of_birth}".replace("00:00:00","").strip
            "xp": player.xp
            "class": player.cls
        }for player in players]

    def from_json(self, list_of_dict):
        return [
            Player(dict["nickname"],dict["email"],dict["date_of_birth"],dict["xp"],dict["class"])
        for dict in list_of_dict]
    
    def from_xml(self, xml_string):
        root = et.fromstring(xml_string)
        players = []
        for data in list(root):
            nickname, email, date_of_birth, xp, cls = [player.text for player in list(data)]
            players.append(Player(nickname, email, date_of_birth, xp, cls))
        return players

    def to_xml(self, players):
        root = et.Element("data")
        for pl in players:
            player = et.SubElement(root, "player")
            nickname = et.SubElement(player, "nickname")
            nickname.text = pl.nickname
            email = et.SubElement(player, "email")
            email.text = pl.email
            date_of_birth = et.SubElement(player, "date_of_birth")
            date_of_birth.text = f"{pl.date_of_birth}".replace("00:00:00", "").strip()
            xp = et.SubElement(player, "xp")
            xp.text = str(pl.xp)
            classes = et.SubElement(player, "class")
            classes.text = pl.cls
        
        return et.tostring(root, "utf-8")

    def from_protobuf(self, binary):

        pass

    def to_protobuf(self, players):

        pass