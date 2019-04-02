import os
import asyncio
import json
import time

import aiohttp
import websockets

import showdown_commands

#not very "thread safe or exception safe" yet xd

class Showdown:

    def __init__(self, bot, id, pw, ai=False, timeout=3600):
        self.bot = bot
        self.id = id
        self.pw = pw
        self.ai = ai
        self.timeout = timeout
        
        self.ws = None
        self.timer = self.timeout
        self.bot_time = 0
        
        showdown_commands.load_commands(self.bot, self)
    
    def reset_time(self):
        self.timer = self.timeout
    
    async def check_timeout(self):
        while True:
            await asyncio.sleep(self.timer)
            self.timer = time.time() - self.bot_time
            if self.timer >= self.timeout:
                pass #timeout occurred #should return here
            else:
                self.timer = self.timeout - self.timer
    
    async def test(self, ctx):
        await ctx.send('test2')
        
    async def login(self, r):
        login_msg = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = r[2] + '|' + r[3]
            
            #assume no errors here (bad idea)
            #login fails if nametaken with bad password->bad challstr
            async with session.post(url, data=data) as response:
                s = json.loads((await response.text())[1:])
                login_msg += s['assertion']
        
        await self.ws.send(login_msg)
        await self.ws.send('|/avatar 27')
        
    async def handle_challenge(self, r):
        
        dict = json.loads(r[2])
        for user, format in dict['challengesFrom'].items():
            if user == 'psikh0':
                # TEAM = 'Toxapex||blacksludge|H|scald,toxicspikes,recover,haze|Calm|252,,4,,252,||,0,,,,|||]Reuniclus||leftovers|1|acidarmor,calmmind,psyshock,recover|Bold|252,,212,,,44||,0,,,,|||]Celesteela||leftovers||leechseed,protect,heavyslam,flamethrower|Sassy|248,,28,,232,|||||]Flygon||brightpowder||defog,uturn,hiddenpowerice,earthquake|Naive|,252,4,,,252|||||]Alakazam||alakazite|H|taunt,recover,psychic,focusblast|Timid|,,4,252,,252||,0,,,,|||]Kyurem||leftovers||substitute,roost,icebeam,earthpower|Timid|56,,,200,,252||,0,,,,|||'
                await self.ws.send('|/utm ' + 'null')
                await self.ws.send('|/accept psikh0')
        return        
    
    async def switch(self, num):
        await self.ws.send(self.room + '|/choose switch ' + num)
    
    #TODO: differentiate between battle messages and others
    
    #room responses always start with >ROOMID\n
    async def handle_room_response(self, response):
        room = response.split('|')[0][1:].rstrip()
    
    #lobby / global responses
    async def handle_global_response(self, response):
        r = response.split('|')
        if len(r) == 1: return
        
        if r[1] == 'challstr':
            await self.login(r)
        elif r[1] == 'updatechallenges':
            await self.handle_challenges(r)
        elif r[1] == 'updatesearch':
            pass
        else:
            return
    
    async def handle_response(self, response):
        #battle room ?
        if response[0] == '>':
            await self.handle_room_response(response)
        else:
            await self.handle_global_response(response)
        
        # elif response_type == 'turn':
            # await ws.send(room + '|/choose move 1')
    
    async def run_timeout_instance(self, ctx):
        if self.ws is not None:
            return
            
        async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as self.ws:
            #handle connectionclosed error
            #can also try: await asyncio.wait_for(ws.recv(), timeout=X)
            async for response in self.ws:
                self.handle_response(response)
               
    async def close():
        self.ws.close()
    