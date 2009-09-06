# Getanewdaddy: kick

import re
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class getanewdaddy(loadable):
    """Remove sponsorship of a member. Their access will be reduced to "galmate" level. Anyone is free to sponsor the person back under the usual conditions. This isn't a kick and it's not final.""" 
    usage = " pnick"
    paramre = re.compile(r"\s(\S+)")
    
    @loadable.require_user
    def execute(self, message, user, params):

        # do stuff here
        idiot = User.load(name=params.group(1), session=session)
        if (idiot is None) or not idiot.is_member():
            print idiot.is_member()
            print idiot.access
            
            message.reply("That idiot isn't a member!")
            return
        if (not user.is_admin()) and idiot.sponsor != user.name:
            message.reply("You are not %s's sponsor"%(idiot.name,))
            return
        
        if "galmate" in Config.options("Access"):
            idiot.access = Config.getint("Access","galmate")
        else:
            idiot.access = 0
        session.commit()
        message.privmsg('remuser %s %s'%(Config.get("Alliance","home"), idiot.name,),'p')
        message.privmsg("ban %s *!*@%s.users.netgamers.org Your sponsor doesn't like you anymore"%(Config.get("Alliance","home"), idiot.name,),'p')
        if idiot.sponsor != user.name:
            message.privmsg("note send %s Some admin has removed you for whatever reason. If you still wish to be a member, go ahead and find someone else to sponsor you back."%(idiot.name,),'p')
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel. %s is no longer %s's sponsor. If anyone else would like to sponsor that person back, they may."%(idiot.name,idiot.sponsor,idiot.name))
        else:
            message.privmsg("note send %s Your sponsor (%s) no longer wishes to be your sponsor. If you still wish to be a member, go ahead and find someone else to sponsor you back."%(idiot.name,user.name,),'p')
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel. You are no longer %s's sponsor. If anyone else would like to sponsor that person back, they may."%(idiot.name,idiot.name))
