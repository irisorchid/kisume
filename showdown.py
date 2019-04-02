import os
import asyncio
import json
import time

import aiohttp
import websockets

from dotenv import load_dotenv

#load_dotenv(verbose=True)

#lets try class based approach
#eventually change this into async class instead of 1 function does all maybe

#not very "thread safe or exception safe" yet xd

bot2 = "d"

class Showdown:

    #timeout = logoff after X seconds?
    #ai = if true make bot play, if false users play
    def __init__(self, bot, id, pw, ai=False, timeout=3600):
        self.id = id
        self.pw = pw
        self.timeout = timeout
        self.ai = ai
        #self.battles = set()
        
    async def test(self, ctx):
        await ctx.send('test2')
        
    async def pick_avatar(self, ws):
        await ws.send('|/avatar 27')
        
    async def login(self, r):
        login_predicate = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = r[2] + '|' + r[3]
            
            #assume no errors here (bad idea)
            #login fails if nametaken with bad password->bad challstr
            async with session.post(url, data=data) as resp:
                r = json.loads((await resp.text())[1:])
                login_predicate += r['assertion']
        
        return login_predicate
        
    async def handle_challenge(self, ws, r):
        #print('alwekjfaslf')
        
        dict = json.loads(r[2])
        print(dict)
        for user, format in dict['challengesFrom'].items():
            if user == 'psikh0':
                print('kusoge1')
                TEAM = 'Toxapex||blacksludge|H|scald,toxicspikes,recover,haze|Calm|252,,4,,252,||,0,,,,|||]Reuniclus||leftovers|1|acidarmor,calmmind,psyshock,recover|Bold|252,,212,,,44||,0,,,,|||]Celesteela||leftovers||leechseed,protect,heavyslam,flamethrower|Sassy|248,,28,,232,|||||]Flygon||brightpowder||defog,uturn,hiddenpowerice,earthquake|Naive|,252,4,,,252|||||]Alakazam||alakazite|H|taunt,recover,psychic,focusblast|Timid|,,4,252,,252||,0,,,,|||]Kyurem||leftovers||substitute,roost,icebeam,earthpower|Timid|56,,,200,,252||,0,,,,|||'
                await ws.send('|/utm ' + 'null')
                await ws.send('|/accept psikh0')
        return        
    
    async def switch(self, num):
        await self.ws.send(self.room + '|/choose switch ' + num)
    
    async def handle_battle: pass
    
    async def handle_response(self, ws, r, room):
        if len(r) == 1:
            return
        response_type = r[1]
        #switch = {}
        """
        elif response_type == 'updatesearch':
            dict = json.loads(r[2])
            if dict['games'] is not None:
                for game, format in dict.items():
                    self.battles.add(game)"""
        #print('command is:' + response_type)
        if response_type == 'challstr':
            #assume not logged on yet
            msg = await self.login(r)
            await ws.send(msg)
            await self.pick_avatar(ws)
        elif response_type == 'updatechallenges':
            await self.handle_challenge(ws, r)
            #print(r[2])
            #print(json.loads(r[2])['challengesFrom'])
        elif response_type == 'turn':
            print(room + ' HELLODISCORD')
            await ws.send(room + '|/choose move 1')
        else:
            return
    
    async def run_timeout_instance(self, ctx):
        if self.ws is not None:
            return
            
        async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as self.ws:
            #handle connectionclosed error
            async for response in self.ws:
                #print(response + ' ENDRESPONSE')
                #lobby responses always start with >
                if response[0] == '>':
                    room = response.split('|')[0][1:].rstrip()
                self.room = room
                """
                for line in response.split('\n'):
                    print(line + ' ENDLINE')
                    await self.handle_response(self.ws, line.split('|'), room)
                    """
               
    async def close():
        self.ws.close()
    