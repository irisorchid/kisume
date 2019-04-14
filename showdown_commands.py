def load_commands(bot, showdown):
    
    @bot.command(name='showdown')
    async def pokemon(ctx):
        if ctx.channel.id != showdown.channel_id: return
        #bot.loop.create_task #timeout task

        if showdown.running:
            print('showdown already running') #debug purposes
            return
        showdown.running = True
        try:
            await showdown.connect_with_timeout(ctx)
        finally:
            showdown.running = False

    @bot.command()
    async def showdown_close(ctx):
        await showdown.close()

def generate_showdown_commands(bot, showdown, ctx):

    async def showdown_commands(message):
        if message.author != bot.user and message.channel == ctx.channel and message.content.startswith('~'):
            if not ctx.channel.id in showdown.rooms: return
            room = showdown.rooms[ctx.channel.id]
            if room is None: return
            
            args = message.content.lower().split(' ')
            command = args[0][1:]
            target = args[1]
            
            #TODO: only allow queue random for now
            if command == 'queue': return
            
            if command == 'switch':
                return await showdown.choose(room, command, target)
            if command == 'move':
                option = ''
                if len(args) > 2:
                    if args[2] == 'mega':
                        option = ' mega'
                    elif args[2] == 'zmove':
                        option = ' zmove'
                return await showdown.choose(room, command, target, option)
            
    return showdown_commands
    
def load_showdown_commands(bot, showdown, ctx):
    if ctx.channel.id in showdown.listener: return
    showdown_commands = generate_showdown_commands(bot, showdown, ctx)
    showdown.listener[ctx.channel.id] = showdown_commands
    bot.add_listener(showdown_commands, 'on_message')

def unload_showdown_commands(bot, showdown, ctx):
    showdown_commands = showdown.listener.pop(ctx.channel.id, None)
    if showdown_commands is not None:
        bot.remove_listener(showdown_commands, 'on_message')