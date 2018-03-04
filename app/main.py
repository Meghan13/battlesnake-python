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
    'name': 'snakesonaboard'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    #x = json.loads(data)
    for foods in data['food']['data']:
        print foods['x']
        print foods['y']


    goalFood = data['food']['data'][0]
    badSpots = []

    for snakes in data['snakes']['data']:
        for point in snakes['body']['data']:
            badSpots.append(point)



    #print json.dumps(data,indent=4) 

    currPosHeadX = data['you']['body']['data'][0]['x']
    currPosHeadY = data['you']['body']['data'][0]['y']

    directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)


    start = (currPosHeadX, currPosHeadY)
    startL = (start[0]+1,start[1])
    startR = (start[0]-1,start[1])   	
    startU = (start[0],start[1]-1)
    startD = (start[0],start[1]+1)

    canGoL = True
    canGoR = True
    canGoU = True
    canGoD = True

    if startL in badSpots:
        canGoL = False

    if startR in badSpots:
        canGoR = False

    if startU in badSpots:
        canGoU = False

    if startD in badSpots:
        canGoD = False


    if(goalFood['x'] < currPosHeadX and canGoL):
        direction = 'left'

    if(goalFood['x'] > currPosHeadX and canGoR):
        direction = 'right'

    if(goalFood['y'] < currPosHeadY and canGoU):
        direction = 'up'

    if(goalFood['y'] > currPosHeadY and canGoD):
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