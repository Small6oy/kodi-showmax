import os, sys, urllib, xbmcplugin, xbmcaddon
from xbmcswift import download_page, xbmc, xbmcgui
from addon.common.addon import Addon
try:
    import json
except ImportError:
    import simplejson as json

addon_id='plugin.video.showmax'
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))

selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)

API_BASE = 'https://api.showmax.com/v36.0/website/catalogue/'
seriesurl = 'search?lang=eng&num=50&type=tv_series'
moviesurl = 'search?lang=eng&num=50&type=movie'
#https://api.showmax.com/v24.0/website/catalogue/search?lang=eng&num=30&start=60

def cat():
    addDir('Search','',1,icon,fanart,'')
    addDir('Series',seriesurl,2,icon,fanart,'')
    addDir('Movies',moviesurl,6,icon,fanart,'')
    addDir('Language','',3,icon,fanart,'')
    addDir('Categories','',4,icon,fanart,'')
    addDir('Sections','',5,icon,fanart,'')  

def Search():
    keyb = xbmc.Keyboard('', 'Search')
    keyb.doModal()    
    if (keyb.isConfirmed()):
        search = keyb.getText().replace(' ','+')
        if (search):            
            url = 'search?lang=eng&q='+search
            Videos(url)
        else:
            cat()

def Movies(url):
    url = API_BASE + url
    src = download_page(url)
    movies = json.loads(src)

    for movie in movies['items']:
        name = movie['title']       
        url = ''
        icon = movie['images'][2]['link']
        thumb = movie['images'][1]['link']
        banner = movie['images'][3]['link']
        fanart = movie['images'][0]['link']  
        description = movie['description']       
        addDir(name,url,3,icon,fanart,description)
    

def Series(url):
    url = API_BASE + url
    src = download_page(url)
    series = json.loads(src)

    for a in series['items']:
        name = a['title']
        url = a['link']
        icon = a['images'][2]['link']
        thumb = a['images'][1]['link']
        banner = a['images'][3]['link']
        fanart = a['images'][0]['link'] 
        description = a['description']     
        addDir3(name,url,3,icon,fanart,thumb,banner,series['count'])
    

def Videos(url):
    url = API_BASE + url
    src = download_page(url)
    series = json.loads(src)

    for a in series['items']:
        name = a['title']
        url = a['link']
        icon = a['images'][2]['link']
        thumb = a['images'][1]['link']
        banner = a['images'][3]['link']
        fanart = a['images'][0]['link'] 
        description = a['description']
        addDir(name,url,3,thumb,fanart,description)  
    setView('videos', 'WideList')

def Language():
    url = API_BASE + 'languages?lang=eng'
    src = download_page(url)
    languages = json.loads(src)

    for lang in languages:        
        addDir(lang['name'],'search?lang=eng&audio_language='+lang['iso_639_3'],7,icon,fanart,'')

def Categories():
    url = API_BASE + 'categories?lang=eng'
    src = download_page(url)
    categories = json.loads(src)

    for cat in categories['items'][0]['child_categories']:
        addDir(cat['title'],'search?lang=eng&category='+cat['id'],7,icon,fanart,'')

def Sections():
    url = API_BASE + 'sections?lang=eng'
    src = download_page(url)
    sections = json.loads(src)

    for sect in sections['items']:
        addDir(sect['name'],'search?lang=eng&section[]='+sect['slug'],7,icon,fanart,'')

def link(url):
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(str(url))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                            
    return param

def addDir(name,url,mode,iconimage,fanart,description):
    
    xbmc.log(url)    
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus('')
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
    liz.setProperty('fanart_image', fanart)
    liz.setProperty('tvshowthumb', iconimage)
    liz.setProperty( "player.art", iconimage)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir2(name,url,mode,poster,fanart,thumb,banner,itemcount):    
    contextMenuItems = []
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)    
    liz.setArt({ 'thumb': thumb, 'poster': poster, 'fanart' : fanart, 'banner ' : banner  })        
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
    return ok

def addDir3(name,url,mode,poster,fanart,thumb,banner,itemcount):
        
    contextMenuItems = []
    contextMenuItems.append(('Series Information', 'XBMC.Action(Info)'))
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)    
    liz.setArt({ 'thumb': thumb, 'poster': poster, 'fanart' : fanart, 'banner ' : banner  })        
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
    return ok

def addDir4(name,url,mode,poster,fanart,thumb,banner,itemcount):
    
    contextMenuItems = []
    contextMenuItems.append(('Videos Information', 'XBMC.Action(Info)'))
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)    
    liz.setArt({ 'thumb': thumb, 'poster': poster, 'fanart' : fanart, 'banner ' : banner  })        
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
    return ok

def notification(title, message, icon):
    addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
    return

def setView(content, viewType):
        
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':
        
        if viewType == 'Info':
            VT = '504'
        elif viewType == 'Info2':
            VT = '503'
        elif viewType == 'Info3':
            VT = '515'
        elif viewType == 'Fanart':
            VT = '508'
        elif viewType == 'PosterWrap':
            VT = '501'
        elif viewType == 'BigList':
            VT = '51'
        elif viewType == 'WideList':
            VT = '499'            
        elif viewType == 'default-view':
            VT = addon.get_setting(viewType)
                
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None:
    cat()

elif mode==1:
    Search()

elif mode==2:
    Series(url)

elif mode==3:
    Language()

elif mode==4:
    Categories()

elif mode==5:
    Sections()

elif mode==6:
    Movies(url)

elif mode==7:
    Videos(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
