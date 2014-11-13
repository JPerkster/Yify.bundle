NAME = 'Yify'
BASE_URL = 'http://yify.tv'
RELEASES_URL = '%s/files/releases/page/%%d/?meta_key=imdbRating&orderby=meta_value&order=desc' % BASE_URL
POPULAR_URL = '%s/popular/page/%%d/?meta_key=imdbRating&orderby=meta_value&order=desc' % BASE_URL
TOP250_URL = '%s/files/movies/page/%%d/?meta_key=imdbRating&orderby=meta_value&order=desc' % BASE_URL
GENRE_URL = '%s/genre/%%s/page/%%%%d/' % BASE_URL
LANGUAGE_URL = '%s/languages/%%s/page/%%%%d/' % BASE_URL 

RE_POSTS = Regex('var posts = ({.+});')

ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

####################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
	HTTP.Headers['Referer'] = 'http://yify.tv/'

####################################################################################################
@handler('/video/yify', NAME, thumb=ICON, art=ART)
def MainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Releases', url=RELEASES_URL), title='Releases'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Popular', url=POPULAR_URL), title='Popular'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Top +250', url=TOP250_URL), title='Top +250'))
	oc.add(DirectoryObject(key = Callback(ListGenres), title='Genres'))
	oc.add(DirectoryObject(key = Callback(ListLanguages), title='Languages'))
	oc.add(DirectoryObject(key = Callback(Watchlist), title='Watchlist'))
	oc.add(SearchDirectoryObject(identifier='com.plexapp.plugins.yify', title='Search', summary='Search Movies on Yify', prompt='Search for...'))

	if Client.Product != 'PlexConnect':
		oc.add(PrefsObject(title='Preferences'))

	return oc

####################################################################################################
@route('/video/yify/listmovies', page=int)
def ListMovies(title, url, page=1):

	oc = ObjectContainer(title2=title)
	data = HTTP.Request(url % page).content
	json = RE_POSTS.search(data)

	html = HTML.ElementFromString(data)

	if json:
		json_obj = JSON.ObjectFromString(json.group(1))

		for movie in json_obj['posts']:

			movie_url = movie['link']
			movie_title = movie['title']
			movie_thumb = movie['image']

			try: movie_summary = movie['post_content']
			except: movie_summary = None

			try: year = int(movie['year'])
			except: year = None

			oc.add(MovieObject(
				url = movie_url,
				title = movie_title,
				summary = movie_summary,
				thumb = Resource.ContentsOfURLWithFallback(url=movie_thumb, fallback='icon-default.jpg')
			))

	else:
		for movie in html.xpath('//article[@class="posts3"]'):

			movie_url = movie.xpath('.//img/parent::a/@href')[0]
			movie_title = movie.xpath('.//h2/text()')[0]
			movie_thumb = movie.xpath('.//img/@src')[0]

			try: movie_summary = movie.xpath('.//h1/text()')[0].split('\n')[0].strip()
			except: movie_summary = None

			try: year = int(movie.xpath('.//h2//a/text()')[0])
			except: year = None

			oc.add(MovieObject(
				url = movie_url,
				title = movie_title,
				summary = movie_summary,
				thumb = Resource.ContentsOfURLWithFallback(url=movie_thumb, fallback='icon-default.jpg')
			))

	if len(html.xpath('//a[@class="nextpostslink"]')) > 0:

		if page % 5 != 0:
			oc.extend(ListMovies(title=title, url=url, page=page+1))

		else:
			oc.add(NextPageObject(
				key = Callback(ListMovies, title=title, url=url, page=page+1),
				title = L('More...')
			))

	return oc

####################################################################################################
@route('/video/yify/listgenres')
def ListGenres():

	oc = ObjectContainer(title2='Genres')

	oc.add(DirectoryObject(key = Callback(ListMovies, title='Action', url=GENRE_URL % 'action'), title='Action'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Animation', url=GENRE_URL % 'animation'), title='Animation'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Comedy', url=GENRE_URL % 'comedy'), title='Comedy'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Documentary', url=GENRE_URL % 'documentary'), title='Documentary'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Drama', url=GENRE_URL % 'drama'), title='Drama'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Family', url=GENRE_URL % 'family'), title='Family'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Horror', url=GENRE_URL % 'horror'), title='Horror'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Mystery', url=GENRE_URL % 'mystery'), title='Mystery'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Romance', url=GENRE_URL % 'romance'), title='Romance'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Science fiction', url=GENRE_URL % 'sci-fi'), title='Science fiction'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Thriller', url=GENRE_URL % 'thriller'), title='Thriller'))

	return oc

####################################################################################################
@route('/video/yify/listlanguages')
def ListLanguages():

	oc = ObjectContainer(title2='Languages')

	oc.add(DirectoryObject(key = Callback(ListMovies, title='Arabic', url=LANGUAGE_URL % 'arabic'), title='Arabic'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Bulgarian', url=LANGUAGE_URL % 'bulgarian'), title='Bulgarian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Chinese', url=LANGUAGE_URL % 'chinese'), title='Chinese'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Croatian', url=LANGUAGE_URL % 'croatian'), title='Croatian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Dutch', url=LANGUAGE_URL % 'dutch'), title='Dutch'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='English', url=LANGUAGE_URL % 'english'), title='English'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Finnish', url=LANGUAGE_URL % 'finnish'), title='Finnish'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='French', url=LANGUAGE_URL % 'french'), title='French'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='German', url=LANGUAGE_URL % 'german'), title='German'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Greek', url=LANGUAGE_URL % 'greek'), title='Greek'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Hebrew', url=LANGUAGE_URL % 'hebrew'), title='Hebrew'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Hindi', url=LANGUAGE_URL % 'hindi'), title='Hindi'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Hungarian', url=LANGUAGE_URL % 'hungarian'), title='Hungarian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Icelandic', url=LANGUAGE_URL % 'icelandic'), title='Icelandic'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Italian', url=LANGUAGE_URL % 'italian'), title='Italian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Japanese', url=LANGUAGE_URL % 'japanese'), title='Japanese'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Korean', url=LANGUAGE_URL % 'korean'), title='Korean'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Norwegian', url=LANGUAGE_URL % 'norwegian'), title='Norwegian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Persian', url=LANGUAGE_URL % 'persian'), title='Persian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Polish', url=LANGUAGE_URL % 'polish'), title='Polish'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Portuguese', url=LANGUAGE_URL % 'portuguese'), title='Portuguese'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Punjabi', url=LANGUAGE_URL % 'punjabi'), title='Punjabi'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Romanian', url=LANGUAGE_URL % 'romanian'), title='Romanian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Russian', url=LANGUAGE_URL % 'russian'), title='Russian'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Spanish', url=LANGUAGE_URL % 'spanish'), title='Spanish'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Swedish', url=LANGUAGE_URL % 'swedish'), title='Swedish'))
	oc.add(DirectoryObject(key = Callback(ListMovies, title='Turkish', url=LANGUAGE_URL % 'turkish'), title='Turkish'))

	return oc

####################################################################################################
@route('/video/yify/watchlist')
def Watchlist():

	if not Login():
		return ObjectContainer(header="Login failed", message="Check your username and password")

	oc = ObjectContainer(title2='Watchlist', no_cache=True)

	post_values = {
		'a': 'get_lists',
		'ajax': '1'
	}

	cookies = HTTP.CookiesForURL(BASE_URL)
	json_obj = JSON.ObjectFromURL(BASE_URL, values=post_values, headers={'Cookie': cookies})

	for list in json_obj:
		id = list['ID']
		title = list['titulo']

		oc.add(DirectoryObject(key = Callback(WatchlistMovies, id=id, title=title), title=title))

	return oc

####################################################################################################
@route('/video/yify/watchlistmovies')
def WatchlistMovies(id, title):

	if not Login():
		return ObjectContainer(header="Login failed", message="Check your username and password")

	oc = ObjectContainer(title2=title, no_cache=True)

	post_values = {
		'listid': id,
		'a': 'get_posts_from_list',
		'ajax': '1'
	}

	cookies = HTTP.CookiesForURL(BASE_URL)
	json_obj = JSON.ObjectFromURL(BASE_URL, values=post_values, headers={'Cookie': cookies})

	for movie in json_obj['posts']:

		if not 'ID' in movie or not 'link' in movie or not 'title' in movie or not 'image' in movie:
			continue

		movie_url = movie['link']
		movie_title = movie['title']
		movie_thumb = movie['image']

		try: movie_summary = movie['post_content']
		except: movie_summary = None

		try: year = int(movie['year'])
		except: year = None

		oc.add(MovieObject(
			url = movie_url,
			title = movie_title,
			summary = movie_summary,
			thumb = Resource.ContentsOfURLWithFallback(url=movie_thumb, fallback='icon-default.jpg')
		))

	return oc

####################################################################################################
@route('/video/yify/login')
def Login():

	if Prefs['username'] and Prefs['password']:

		HTTP.ClearCookies()

		post_values = {
			'log': Prefs['username'],
			'pwd': Prefs['password'],
			'a': 'login',
			'ajax': '1'
		}

		json = HTTP.Request(BASE_URL, values=post_values).content
		json = json.replace("'", '"')
		json_obj = JSON.ObjectFromString(json)

		if 'status' in json_obj and json_obj['status'] == 'OK':
			return True

	return False
