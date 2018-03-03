import bottle
import os
import random
import json


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    #print bottle
    #print "TEST"
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'dallas'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    print
    print
    #x = json.loads(data)
    for foods in data['food']['data']:
        print foods['x']
        print foods['y']
        print

    goalFood = data['food']['data'][0]

    #print json.dumps(data,indent=4) 
    
    currPosHeadX = data['you']['body']['data'][0]['x']
    currPosHeadY = data['you']['body']['data'][0]['y']

    directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)

    if(goalFood['x'] < currPosHeadX):
        direction = 'left'
    
    if(goalFood['x'] > currPosHeadX):
        direction = 'right'
    
    if(goalFood['y'] < currPosHeadY):
        direction = 'up'
    
    if(goalFood['y'] > currPosHeadY):
        direction = 'down'

    #print direction
    return {
        'move': direction,
        'taunt': 'For the Horde!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)