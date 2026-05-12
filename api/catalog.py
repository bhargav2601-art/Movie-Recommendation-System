from __future__ import annotations

from copy import deepcopy
from datetime import date
from urllib.parse import quote


DEFAULT_TRAILER_WATCH = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
DEFAULT_TRAILER_PLACEHOLDER = "/assets/hero.png"

PAYMENT_METHODS = [
    {"name": "UPI", "description": "Pay instantly with GPay, PhonePe, Paytm, or BHIM."},
    {"name": "Credit / Debit Card", "description": "Visa, Mastercard, RuPay, and Amex accepted."},
    {"name": "Net Banking", "description": "All major banks with secure 3D verification."},
    {"name": "Wallets", "description": "Use wallet balance and reward cashbacks."},
]

FOOD_COMBOS = [
    {"id": "combo-popcorn", "name": "Signature Popcorn Combo", "price": 420, "items": ["Large caramel popcorn", "2 soft drinks"]},
    {"id": "combo-recliner", "name": "Recliner Luxe Box", "price": 590, "items": ["Cheese nachos", "Cold coffee", "Chocolate bites"]},
    {"id": "combo-quick", "name": "Quick Bite Duo", "price": 310, "items": ["Salted popcorn", "Coke"]},
]

COUPONS = [
    {"code": "CINEVERSE100", "discount": 100, "description": "Flat discount on orders above INR 999"},
    {"code": "IMAX20", "discountPercent": 20, "description": "20% off on IMAX ticket basket"},
]

CITY_AREAS = {
    "Bangalore": ["Orion Mall", "Koramangala", "Whitefield", "JP Nagar", "MG Road", "Electronic City"],
    "Mumbai": ["Lower Parel", "Phoenix Mall", "Bandra", "Andheri", "Powai", "Navi Mumbai"],
    "Delhi": ["Saket", "Rajouri Garden", "Connaught Place", "Noida", "Dwarka", "Vasant Kunj"],
    "Hyderabad": ["Banjara Hills", "Kukatpally", "Gachibowli", "Madhapur", "Secunderabad", "Ameerpet"],
    "Chennai": ["Velachery", "Anna Nagar", "OMR", "T Nagar", "Vadapalani", "Nungambakkam"],
    "Pune": ["Viman Nagar", "Hinjawadi", "Kothrud", "Wakad", "Baner", "Aundh"],
}

THEATER_PHOTOS = {
    "PVR": "/assets/theaters/pvr.svg",
    "INOX": "/assets/theaters/inox.svg",
    "Cinepolis": "/assets/theaters/cinepolis.svg",
    "Miraj": "/assets/theaters/miraj.svg",
    "Carnival": "/assets/theaters/carnival.svg",
    "Asian Cinemas": "/assets/theaters/asian-cinemas.svg",
}

THEATER_FACILITIES = {
    "PVR": ["Gourmet snacks", "Luxury recliners", "Laser projection", "Lounge access"],
    "INOX": ["Dolby Atmos", "Contactless entry", "Gourmet cafe", "Wheelchair access"],
    "Cinepolis": ["IMAX", "4DX", "Family pods", "Fast check-in"],
    "Miraj": ["Budget combo deals", "Recliner rows", "Ample parking"],
    "Carnival": ["Arcade zone", "Food court tie-ins", "Spacious foyers"],
    "Asian Cinemas": ["Premium Telugu releases", "Lounge recliners", "Valet parking"],
}


def normalize_catalog_key(value: str) -> str:
    return "".join(character for character in value.lower() if character.isalnum())


def actor(name: str, role: str, image: str, imdb_link: str, popularity: float, bio: str, filmography: list[str], other_movies: list[str]):
    return {
        "name": name,
        "role": role,
        "image": image,
        "imdbLink": imdb_link,
        "popularity": popularity,
        "bio": bio,
        "filmography": filmography,
        "otherMovies": other_movies,
    }


def youtube_video_id(url: str | None) -> str | None:
    if not url:
        return None
    if "watch?v=" in url:
        return url.split("watch?v=", 1)[1].split("&", 1)[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/", 1)[1].split("?", 1)[0]
    if "embed/" in url:
        return url.split("embed/", 1)[1].split("?", 1)[0]
    return None


def youtube_embed(url: str) -> str:
    video_id = youtube_video_id(url)
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return ""


def trailer_watch_url(url: str) -> str:
    if "watch?v=" in url or "youtu.be/" in url:
        return url
    if "embed/" in url:
        video_id = url.split("embed/", 1)[1].split("?", 1)[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url or DEFAULT_TRAILER_WATCH


def youtube_thumbnail(url: str) -> str:
    watch_url = url if "watch?v=" in url else trailer_watch_url(url)
    video_id = youtube_video_id(watch_url)
    if not video_id:
        return DEFAULT_TRAILER_PLACEHOLDER
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"


def asset_bundle(slug: str) -> dict:
    return {
        "poster": f"/assets/movies/{slug}/poster.svg",
        "backdrop": f"/assets/movies/{slug}/backdrop.svg",
        "logo": f"/assets/movies/{slug}/logo.svg",
        "gallery": [
            f"/assets/movies/{slug}/gallery/scene-1.svg",
            f"/assets/movies/{slug}/gallery/scene-2.svg",
            f"/assets/movies/{slug}/gallery/scene-3.svg",
        ],
    }


def actor_image_path(name: str) -> str:
    slug = normalize_catalog_key(name)
    return f"/assets/cast/{slug}.svg"


def build_actor(name: str, role: str, movie_title: str, related_titles: list[str], popularity_seed: int) -> dict:
    popularity = round(72 + (popularity_seed % 25) + 0.3, 1)
    other_movies = [title for title in related_titles if title != movie_title][:3] or related_titles[:3]
    filmography = [movie_title, *other_movies][:3]
    return actor(
        name=name,
        role=role,
        image=actor_image_path(name),
        imdb_link=f"https://www.imdb.com/find/?q={quote(name)}",
        popularity=popularity,
        bio=f"{name} brings star presence and screen-specific energy to {movie_title}.",
        filmography=filmography,
        other_movies=other_movies,
    )


def trailer_variant(title: str, url: str) -> dict:
    return {
        "title": title,
        "trailerUrl": youtube_embed(url),
        "trailerWatchUrl": trailer_watch_url(url),
        "trailerThumbnail": youtube_thumbnail(url),
    }


MOVIE_BLUEPRINTS = [
    {"slug": "baahubali", "title": "Baahubali", "language": ["Telugu", "Hindi", "Tamil", "Malayalam"], "genre": ["Epic", "Adventure", "Drama"], "duration": "2h 39m", "runtimeMinutes": 159, "rating": 9.1, "imdbScore": 8.0, "rottenTomatoes": 89, "certificate": "UA", "storyline": "A mythic warrior saga about destiny, betrayal, and a kingdom built on loyalty, bloodline, and impossible scale.", "cast": [("Prabhas", "Amarendra / Mahendra Baahubali"), ("Rana Daggubati", "Bhallaladeva"), ("Anushka Shetty", "Devasena")], "trailer_watch_url": "https://www.youtube.com/watch?v=hkZNa2JGXMc", "mood": "Mythic action with operatic emotional stakes.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2015-07-10", "trendingBadge": "Epic Rewatch Favorite", "heroTag": "Kingdom-scale fantasy event", "whyRecommended": "Because you enjoy mythic worldbuilding and event cinema.", "palette": {"primary": "#f59e0b", "secondary": "#7c2d12", "accent": "#fde68a"}, "comingSoon": False},
    {"slug": "rrr", "title": "RRR", "language": ["Telugu", "Hindi", "Tamil", "Malayalam"], "genre": ["Action", "Period Drama"], "duration": "3h 7m", "runtimeMinutes": 187, "rating": 9.0, "imdbScore": 7.8, "rottenTomatoes": 95, "certificate": "UA", "storyline": "Two revolutionaries forge a volcanic friendship in a sweeping anti-colonial action spectacle.", "cast": [("N. T. Rama Rao Jr.", "Komaram Bheem"), ("Ram Charan", "Alluri Sitarama Raju"), ("Alia Bhatt", "Sita")], "trailer_watch_url": "https://www.youtube.com/watch?v=NgBoMJy386M", "mood": "Thunderous friendship, rebellion, and musical spectacle.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2022-03-25", "trendingBadge": "Global Blockbuster", "heroTag": "Revolution on a colossal canvas", "whyRecommended": "Because you want theatrical scale and crowd eruptions.", "palette": {"primary": "#dc2626", "secondary": "#1f2937", "accent": "#fca5a5"}, "comingSoon": False},
    {"slug": "salaar", "title": "Salaar", "language": ["Telugu", "Hindi", "Tamil", "Kannada"], "genre": ["Action", "Crime", "Drama"], "duration": "2h 55m", "runtimeMinutes": 175, "rating": 8.8, "imdbScore": 6.6, "rottenTomatoes": 78, "certificate": "A", "storyline": "A brutal promise between brothers-in-arms ignites a war for power in a dystopian empire.", "cast": [("Prabhas", "Deva"), ("Prithviraj Sukumaran", "Varadha"), ("Shruti Haasan", "Aadya")], "trailer_watch_url": "https://www.youtube.com/watch?v=4GPvYMKtrtI", "mood": "Charcoal-black action with volcanic payoffs.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2023-12-22", "trendingBadge": "Mass Action Peak", "heroTag": "Industrial-scale action storm", "whyRecommended": "Because heavy-scale action worlds are your lane.", "palette": {"primary": "#d97706", "secondary": "#111827", "accent": "#fbbf24"}, "comingSoon": False},
    {"slug": "pushpa", "title": "Pushpa: The Rise", "language": ["Telugu", "Hindi", "Tamil", "Malayalam"], "genre": ["Action", "Crime"], "duration": "2h 59m", "runtimeMinutes": 179, "rating": 8.7, "imdbScore": 7.6, "rottenTomatoes": 79, "certificate": "UA", "storyline": "A red sandalwood smuggler rises through violence, swagger, and ruthless survival instincts.", "cast": [("Allu Arjun", "Pushpa Raj"), ("Rashmika Mandanna", "Srivalli"), ("Fahadh Faasil", "Bhanwar Singh Shekhawat")], "trailer_watch_url": "https://www.youtube.com/watch?v=Q1NKMPhP8PY", "mood": "Grit, swagger, and combustible mass energy.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2021-12-17", "trendingBadge": "Mass Phenomenon", "heroTag": "Red sandal rebellion", "whyRecommended": "Because style-heavy antiheroes work for you.", "palette": {"primary": "#b45309", "secondary": "#14532d", "accent": "#facc15"}, "comingSoon": False},
    {"slug": "kalki-2898-ad", "title": "Kalki 2898 AD", "language": ["Telugu", "Hindi", "Tamil", "Malayalam"], "genre": ["Sci-Fi", "Action", "Adventure"], "duration": "3h 1m", "runtimeMinutes": 181, "rating": 8.9, "imdbScore": 7.3, "rottenTomatoes": 83, "certificate": "UA", "storyline": "Ancient prophecy collides with futuristic tyranny in an apocalyptic Indian sci-fi epic.", "cast": [("Prabhas", "Bhairava"), ("Deepika Padukone", "Sumathi"), ("Amitabh Bachchan", "Ashwatthama")], "trailer_watch_url": "https://www.youtube.com/watch?v=BfCIPsEGAS8", "mood": "Mythic futurism designed for giant-format screens.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2024-06-27", "trendingBadge": "Sci-Fi Event", "heroTag": "Myth meets apocalypse", "whyRecommended": "Because you want sci-fi spectacle with Indian mythic texture.", "palette": {"primary": "#38bdf8", "secondary": "#312e81", "accent": "#a5f3fc"}, "comingSoon": False},
    {"slug": "devara", "title": "Devara", "language": ["Telugu", "Hindi", "Tamil"], "genre": ["Action", "Drama"], "duration": "2h 58m", "runtimeMinutes": 178, "rating": 8.6, "imdbScore": 7.1, "rottenTomatoes": 76, "certificate": "UA", "storyline": "A coastal legend rises against betrayal and blood-soaked politics in a sea-bound action drama.", "cast": [("N. T. Rama Rao Jr.", "Devara"), ("Janhvi Kapoor", "Thangam"), ("Saif Ali Khan", "Bhaira")], "trailer_watch_url": "https://www.youtube.com/watch?v=rc61YHl1PFY", "mood": "Stormy shoreline action with simmering vendetta.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2024-09-27", "trendingBadge": "Coastal Action Saga", "heroTag": "Salt, blood, and legacy", "whyRecommended": "Because intense family-action sagas keep landing for you.", "palette": {"primary": "#0ea5e9", "secondary": "#1e3a8a", "accent": "#7dd3fc"}, "comingSoon": False},
    {"slug": "hanu-man", "title": "Hanu-Man", "language": ["Telugu", "Hindi", "Tamil"], "genre": ["Fantasy", "Superhero", "Action"], "duration": "2h 38m", "runtimeMinutes": 158, "rating": 8.5, "imdbScore": 7.8, "rottenTomatoes": 80, "certificate": "UA", "storyline": "A small-town dreamer discovers divine power and becomes an unlikely superhero in a folkloric universe.", "cast": [("Teja Sajja", "Hanumanthu"), ("Amritha Aiyer", "Meenakshi"), ("Vinay Rai", "Michael")], "trailer_watch_url": "https://www.youtube.com/watch?v=Oqvly3MvlXA", "mood": "Folkloric wonder with celebratory superhero beats.", "subtitles": ["English", "Hindi", "Telugu"], "releaseDate": "2024-01-12", "trendingBadge": "Mythic Superhero", "heroTag": "Village hero, divine power", "whyRecommended": "Because you like mythic fantasy with crowd-pleasing heart.", "palette": {"primary": "#22c55e", "secondary": "#14532d", "accent": "#bbf7d0"}, "comingSoon": False},
    {"slug": "pathaan", "title": "Pathaan", "language": ["Hindi", "Tamil", "Telugu"], "genre": ["Action", "Spy Thriller"], "duration": "2h 26m", "runtimeMinutes": 146, "rating": 8.3, "imdbScore": 7.8, "rottenTomatoes": 83, "certificate": "UA", "storyline": "An exiled field operative returns for a globe-spanning mission filled with slick combat and covert alliances.", "cast": [("Shah Rukh Khan", "Pathaan"), ("Deepika Padukone", "Rubina"), ("John Abraham", "Jim")], "trailer_watch_url": "https://www.youtube.com/watch?v=KDzw3esfqaI", "mood": "Explosive espionage with stadium-scale action.", "subtitles": ["English", "Hindi", "Tamil", "Telugu"], "releaseDate": "2023-01-25", "trendingBadge": "Spy Universe Hit", "heroTag": "High-octane chase thriller", "whyRecommended": "Because you like large-format action and franchise spectacles.", "palette": {"primary": "#f97316", "secondary": "#7c2d12", "accent": "#fed7aa"}, "comingSoon": False},
    {"slug": "jawan", "title": "Jawan", "language": ["Hindi", "Tamil", "Telugu"], "genre": ["Action", "Thriller"], "duration": "2h 49m", "runtimeMinutes": 169, "rating": 8.8, "imdbScore": 7.0, "rottenTomatoes": 81, "certificate": "UA", "storyline": "A vigilante mastermind confronts corruption through daring heists and emotional payoffs.", "cast": [("Shah Rukh Khan", "Azad / Vikram Rathore"), ("Nayanthara", "Narmada"), ("Vijay Sethupathi", "Kalee")], "trailer_watch_url": "https://www.youtube.com/watch?v=COv52Qyctws", "mood": "Mass action swagger with emotional spikes.", "subtitles": ["English", "Hindi", "Tamil"], "releaseDate": "2023-09-07", "trendingBadge": "Mass Entertainer", "heroTag": "Vigilante spectacle", "whyRecommended": "Because slick action and emotional reveals are working for you.", "palette": {"primary": "#ef4444", "secondary": "#111827", "accent": "#fca5a5"}, "comingSoon": False},
    {"slug": "animal", "title": "Animal", "language": ["Hindi", "Telugu", "Tamil"], "genre": ["Crime", "Drama", "Action"], "duration": "3h 21m", "runtimeMinutes": 201, "rating": 8.5, "imdbScore": 6.2, "rottenTomatoes": 67, "certificate": "A", "storyline": "A damaged heir's violent hunger for approval detonates into a generational crime saga.", "cast": [("Ranbir Kapoor", "Ranvijay"), ("Rashmika Mandanna", "Geetanjali"), ("Bobby Deol", "Abrar")], "trailer_watch_url": "https://www.youtube.com/watch?v=Dydmpfo68DA", "mood": "Operatic rage, family trauma, and relentless violence.", "subtitles": ["English", "Hindi"], "releaseDate": "2023-12-01", "trendingBadge": "Dark Sensation", "heroTag": "Ferocious father-son spiral", "whyRecommended": "Because intense gangster melodrama keeps pulling you in.", "palette": {"primary": "#991b1b", "secondary": "#1f2937", "accent": "#fca5a5"}, "comingSoon": False},
    {"slug": "fighter", "title": "Fighter", "language": ["Hindi"], "genre": ["Action", "Aerial Drama"], "duration": "2h 46m", "runtimeMinutes": 166, "rating": 8.1, "imdbScore": 6.4, "rottenTomatoes": 75, "certificate": "UA", "storyline": "Elite Air Force pilots face national conflict, personal wounds, and spectacle in the skies.", "cast": [("Hrithik Roshan", "Patty"), ("Deepika Padukone", "Minni"), ("Anil Kapoor", "Rocky")], "trailer_watch_url": "https://www.youtube.com/watch?v=6amIq_mP4xM", "mood": "Jet-powered patriotism with glossy emotional momentum.", "subtitles": ["English", "Hindi"], "releaseDate": "2024-01-25", "trendingBadge": "Aerial Action", "heroTag": "Afterburner spectacle", "whyRecommended": "Because premium-format action is a great fit for your queue.", "palette": {"primary": "#60a5fa", "secondary": "#1d4ed8", "accent": "#bfdbfe"}, "comingSoon": False},
    {"slug": "war", "title": "War", "language": ["Hindi", "Tamil", "Telugu"], "genre": ["Action", "Spy Thriller"], "duration": "2h 34m", "runtimeMinutes": 154, "rating": 8.2, "imdbScore": 6.5, "rottenTomatoes": 72, "certificate": "UA", "storyline": "Mentor and protégé collide in a globetrotting spy action showdown full of sleek reversals.", "cast": [("Hrithik Roshan", "Kabir"), ("Tiger Shroff", "Khalid"), ("Vaani Kapoor", "Naina")], "trailer_watch_url": "https://www.youtube.com/watch?v=tQ0mzXRk-oM", "mood": "Polished spy action with kinetic set pieces.", "subtitles": ["English", "Hindi"], "releaseDate": "2019-10-02", "trendingBadge": "Spy Duel", "heroTag": "Mentor versus protégé", "whyRecommended": "Because slick, muscled espionage is always a safe bet.", "palette": {"primary": "#f59e0b", "secondary": "#111827", "accent": "#fde68a"}, "comingSoon": False},
    {"slug": "dunki", "title": "Dunki", "language": ["Hindi"], "genre": ["Drama", "Comedy"], "duration": "2h 41m", "runtimeMinutes": 161, "rating": 8.0, "imdbScore": 6.8, "rottenTomatoes": 74, "certificate": "UA", "storyline": "A migration odyssey unfolds through friendship, longing, and bittersweet humor across borders.", "cast": [("Shah Rukh Khan", "Hardy"), ("Taapsee Pannu", "Manu"), ("Vicky Kaushal", "Sukhi")], "trailer_watch_url": "https://www.youtube.com/watch?v=ACKQDAlAfFE", "mood": "Warm-hearted drama with crowd-pleasing humor.", "subtitles": ["English", "Hindi"], "releaseDate": "2023-12-21", "trendingBadge": "Feel-Good Drama", "heroTag": "Home, migration, and friendship", "whyRecommended": "Because you want emotional stories without losing star power.", "palette": {"primary": "#14b8a6", "secondary": "#164e63", "accent": "#99f6e4"}, "comingSoon": False},
    {"slug": "stree-2", "title": "Stree 2", "language": ["Hindi"], "genre": ["Horror", "Comedy"], "duration": "2h 29m", "runtimeMinutes": 149, "rating": 8.6, "imdbScore": 7.2, "rottenTomatoes": 84, "certificate": "UA", "storyline": "The town faces another supernatural threat where chaos, laughs, and local folklore collide.", "cast": [("Rajkummar Rao", "Vicky"), ("Shraddha Kapoor", "Unnamed Woman"), ("Pankaj Tripathi", "Rudra")], "trailer_watch_url": "https://www.youtube.com/watch?v=KVnheXywIbY", "mood": "Spooky fun with excellent crowd energy.", "subtitles": ["English", "Hindi"], "releaseDate": "2024-08-15", "trendingBadge": "Horror Crowd Favorite", "heroTag": "Folk horror, louder and wilder", "whyRecommended": "Because comedy-horror gives you a perfect group watch.", "palette": {"primary": "#a855f7", "secondary": "#312e81", "accent": "#ddd6fe"}, "comingSoon": False},
    {"slug": "kgf", "title": "KGF Chapter 1", "language": ["Kannada", "Hindi", "Telugu", "Tamil"], "genre": ["Action", "Period Crime"], "duration": "2h 36m", "runtimeMinutes": 156, "rating": 8.8, "imdbScore": 8.2, "rottenTomatoes": 86, "certificate": "UA", "storyline": "A ruthless underdog claws through the gold fields toward power and mythic legend.", "cast": [("Yash", "Rocky"), ("Srinidhi Shetty", "Reena"), ("Anant Nag", "Anand Ingalagi")], "trailer_watch_url": "https://www.youtube.com/watch?v=-KfsY-qwBS0", "mood": "Dusty, mythic, and ferociously stylish.", "subtitles": ["English", "Hindi", "Kannada"], "releaseDate": "2018-12-21", "trendingBadge": "Kannada Phenomenon", "heroTag": "Gold mine uprising", "whyRecommended": "Because antihero origin stories are your comfort watch.", "palette": {"primary": "#ca8a04", "secondary": "#422006", "accent": "#fde047"}, "comingSoon": False},
    {"slug": "kgf-chapter-2", "title": "KGF Chapter 2", "language": ["Kannada", "Hindi", "Telugu", "Tamil"], "genre": ["Action", "Period Crime"], "duration": "2h 48m", "runtimeMinutes": 168, "rating": 8.9, "imdbScore": 8.2, "rottenTomatoes": 88, "certificate": "UA", "storyline": "Rocky consolidates myth and empire as every alliance fractures under violence and ambition.", "cast": [("Yash", "Rocky"), ("Sanjay Dutt", "Adheera"), ("Raveena Tandon", "Ramika Sen")], "trailer_watch_url": "https://www.youtube.com/watch?v=JKa05nyUmuQ", "mood": "Grand, metallic, and thunderously theatrical.", "subtitles": ["English", "Hindi", "Kannada"], "releaseDate": "2022-04-14", "trendingBadge": "Mass Mania", "heroTag": "Empire at full blast", "whyRecommended": "Because amplified sequels are absolutely your thing.", "palette": {"primary": "#eab308", "secondary": "#1f2937", "accent": "#fef08a"}, "comingSoon": False},
    {"slug": "kantara", "title": "Kantara", "language": ["Kannada", "Hindi", "Telugu", "Tamil"], "genre": ["Folklore", "Thriller", "Drama"], "duration": "2h 30m", "runtimeMinutes": 150, "rating": 8.7, "imdbScore": 8.2, "rottenTomatoes": 93, "certificate": "UA", "storyline": "Land, ritual, and ancestral force collide in a forest-set folklore thriller with spiritual intensity.", "cast": [("Rishab Shetty", "Shiva"), ("Sapthami Gowda", "Leela"), ("Kishore", "Murali")], "trailer_watch_url": "https://www.youtube.com/watch?v=8mrVmf239GU", "mood": "Earthy, immersive, and spiritually charged.", "subtitles": ["English", "Hindi", "Kannada"], "releaseDate": "2022-09-30", "trendingBadge": "Folklore Triumph", "heroTag": "Forest spirit awakening", "whyRecommended": "Because rooted storytelling with intensity keeps surprising you.", "palette": {"primary": "#16a34a", "secondary": "#14532d", "accent": "#86efac"}, "comingSoon": False},
    {"slug": "777-charlie", "title": "777 Charlie", "language": ["Kannada", "Hindi", "Telugu", "Tamil"], "genre": ["Adventure", "Family", "Drama"], "duration": "2h 44m", "runtimeMinutes": 164, "rating": 8.5, "imdbScore": 8.7, "rottenTomatoes": 94, "certificate": "UA", "storyline": "A lonely man and an irrepressible dog transform each other on a healing road journey.", "cast": [("Rakshit Shetty", "Dharma"), ("Sangeetha Sringeri", "Devika"), ("Raj B. Shetty", "Dr. Ashwin")], "trailer_watch_url": "https://www.youtube.com/watch?v=vK4v2M4lreA", "mood": "Heartfelt, scenic, and deeply life-affirming.", "subtitles": ["English", "Hindi", "Kannada"], "releaseDate": "2022-06-10", "trendingBadge": "Family Favorite", "heroTag": "Road trip with soul", "whyRecommended": "Because warm emotional journeys belong on the big screen too.", "palette": {"primary": "#0f766e", "secondary": "#164e63", "accent": "#99f6e4"}, "comingSoon": False},
    {"slug": "leo", "title": "Leo", "language": ["Tamil", "Hindi", "Telugu"], "genre": ["Action", "Thriller"], "duration": "2h 44m", "runtimeMinutes": 164, "rating": 8.4, "imdbScore": 7.2, "rottenTomatoes": 79, "certificate": "A", "storyline": "A cafe owner with a buried past is dragged back into a violent criminal legacy.", "cast": [("Vijay", "Parthiban / Leo"), ("Trisha", "Sathya"), ("Sanjay Dutt", "Antony Das")], "trailer_watch_url": "https://www.youtube.com/watch?v=Po3jStA673E", "mood": "Brooding action with franchise electricity.", "subtitles": ["English", "Hindi", "Tamil"], "releaseDate": "2023-10-19", "trendingBadge": "Loki Universe Heat", "heroTag": "Past life returns with fire", "whyRecommended": "Because morally grey action thrillers fit your taste.", "palette": {"primary": "#7f1d1d", "secondary": "#0f172a", "accent": "#fca5a5"}, "comingSoon": False},
    {"slug": "vikram", "title": "Vikram", "language": ["Tamil", "Hindi", "Telugu"], "genre": ["Action", "Thriller", "Crime"], "duration": "2h 54m", "runtimeMinutes": 174, "rating": 8.8, "imdbScore": 8.3, "rottenTomatoes": 89, "certificate": "UA", "storyline": "A covert task force peels back a narcotics conspiracy linking ghosts, grief, and retribution.", "cast": [("Kamal Haasan", "Vikram"), ("Fahadh Faasil", "Amar"), ("Vijay Sethupathi", "Santhanam")], "trailer_watch_url": "https://www.youtube.com/watch?v=OKBMCL-frPU", "mood": "Precision-built action cinema with veteran swagger.", "subtitles": ["English", "Hindi", "Tamil"], "releaseDate": "2022-06-03", "trendingBadge": "Action Masterclass", "heroTag": "Covert revenge operation", "whyRecommended": "Because layered action thrillers with payoffs are your sweet spot.", "palette": {"primary": "#ef4444", "secondary": "#111827", "accent": "#fecaca"}, "comingSoon": False},
    {"slug": "master", "title": "Master", "language": ["Tamil", "Hindi", "Telugu"], "genre": ["Action", "Drama"], "duration": "2h 59m", "runtimeMinutes": 179, "rating": 8.2, "imdbScore": 7.3, "rottenTomatoes": 76, "certificate": "UA", "storyline": "An unruly professor is posted to a juvenile facility and clashes with a chilling local crime lord.", "cast": [("Vijay", "JD"), ("Vijay Sethupathi", "Bhavani"), ("Malavika Mohanan", "Charulatha")], "trailer_watch_url": "https://www.youtube.com/watch?v=UTiXQcrLlv4", "mood": "Mass-star charisma with bruising confrontations.", "subtitles": ["English", "Hindi", "Tamil"], "releaseDate": "2021-01-13", "trendingBadge": "Star Showdown", "heroTag": "Teacher versus kingpin", "whyRecommended": "Because high-voltage hero-villain battles always land.", "palette": {"primary": "#f97316", "secondary": "#7c2d12", "accent": "#fdba74"}, "comingSoon": False},
    {"slug": "thunivu", "title": "Thunivu", "language": ["Tamil", "Hindi", "Telugu"], "genre": ["Action", "Heist"], "duration": "2h 25m", "runtimeMinutes": 145, "rating": 7.9, "imdbScore": 6.1, "rottenTomatoes": 69, "certificate": "UA", "storyline": "A mysterious mastermind seizes a bank and exposes larger corruption beneath the spectacle.", "cast": [("Ajith Kumar", "Dark Devil"), ("Manju Warrier", "Kanmani"), ("Samuthirakani", "Dayalan")], "trailer_watch_url": "https://www.youtube.com/watch?v=jnBZboK17_A", "mood": "Glossy heist thrills with antihero confidence.", "subtitles": ["English", "Hindi", "Tamil"], "releaseDate": "2023-01-11", "trendingBadge": "Heist Thriller", "heroTag": "Bank siege with swagger", "whyRecommended": "Because slick antihero capers suit your weekend watch.", "palette": {"primary": "#06b6d4", "secondary": "#164e63", "accent": "#a5f3fc"}, "comingSoon": False},
    {"slug": "jailer", "title": "Jailer", "language": ["Tamil", "Hindi", "Telugu"], "genre": ["Action", "Comedy", "Crime"], "duration": "2h 48m", "runtimeMinutes": 168, "rating": 8.4, "imdbScore": 7.1, "rottenTomatoes": 78, "certificate": "UA", "storyline": "A retired jailer quietly detonates a ruthless rescue mission when his family is threatened.", "cast": [("Rajinikanth", "Tiger Muthuvel Pandian"), ("Vinayakan", "Varman"), ("Ramya Krishnan", "Vijaya")], "trailer_watch_url": "https://www.youtube.com/watch?v=Y5BeWdODPqo", "mood": "Cool-headed star charisma with explosive eruptions.", "subtitles": ["English", "Hindi", "Tamil"], "releaseDate": "2023-08-10", "trendingBadge": "Superstar Reloaded", "heroTag": "Retired legend returns", "whyRecommended": "Because composed swagger and punchy action always travel.", "palette": {"primary": "#facc15", "secondary": "#1f2937", "accent": "#fde68a"}, "comingSoon": False},
    {"slug": "premalu", "title": "Premalu", "language": ["Malayalam", "Hindi", "Tamil"], "genre": ["Romance", "Comedy"], "duration": "2h 36m", "runtimeMinutes": 156, "rating": 8.5, "imdbScore": 8.0, "rottenTomatoes": 95, "certificate": "U", "storyline": "A drifting young man lands in Hyderabad and finds sharp, charming romance in everyday life.", "cast": [("Naslen", "Sachin"), ("Mamitha Baiju", "Reenu"), ("Sangeeth Prathap", "Amal Davis")], "trailer_watch_url": "https://www.youtube.com/watch?v=rR_2ti4l3nM", "trailer_variants": [trailer_variant("Premalu", "https://www.youtube.com/watch?v=rR_2ti4l3nM"), trailer_variant("Premalu Telugu", "https://www.youtube.com/watch?v=V9vOryQXbcY"), trailer_variant("Premalu Malayalam", "https://www.youtube.com/watch?v=ix5t4hT6qrg")], "mood": "Fresh, playful, and instantly lovable.", "subtitles": ["English", "Hindi", "Malayalam"], "releaseDate": "2024-02-09", "trendingBadge": "Rom-Com Delight", "heroTag": "Modern love, local flavor", "whyRecommended": "Because breezy romance with personality feels right.", "palette": {"primary": "#fb7185", "secondary": "#7e22ce", "accent": "#fbcfe8"}, "comingSoon": False},
    {"slug": "aavesham", "title": "Aavesham", "language": ["Malayalam", "Hindi", "Tamil"], "genre": ["Action", "Comedy"], "duration": "2h 38m", "runtimeMinutes": 158, "rating": 8.6, "imdbScore": 7.9, "rottenTomatoes": 88, "certificate": "UA", "storyline": "Three students stumble into the orbit of a larger-than-life gangster who becomes their chaotic guardian angel.", "cast": [("Fahadh Faasil", "Ranga"), ("Hipzster", "Aju"), ("Mithun Jai Shankar", "Bibi")], "trailer_watch_url": "https://www.youtube.com/watch?v=8lyGmP4fEEM", "mood": "Wildly funny, stylish, and unhinged in the best way.", "subtitles": ["English", "Hindi", "Malayalam"], "releaseDate": "2024-04-11", "trendingBadge": "Cult Energy", "heroTag": "Gangster comedy chaos", "whyRecommended": "Because anarchic comedy with star power is irresistible.", "palette": {"primary": "#f97316", "secondary": "#7f1d1d", "accent": "#fdba74"}, "comingSoon": False},
    # TRAILER DATABASE CORRECTION:
    # Replace legacy Batman Part II and Manjummel Boys placeholders with the updated official links.
    {"slug": "manjummel-boys", "title": "Manjummel Boys", "language": ["Malayalam", "Hindi", "Tamil"], "genre": ["Survival", "Adventure", "Drama"], "duration": "2h 15m", "runtimeMinutes": 135, "rating": 8.7, "imdbScore": 8.3, "rottenTomatoes": 96, "certificate": "UA", "storyline": "A carefree trip turns into a nerve-shredding survival mission rooted in friendship and courage.", "cast": [("Soubin Shahir", "Siju David"), ("Sreenath Bhasi", "Subash"), ("Balu Varghese", "Sixen")], "trailer_watch_url": "https://youtu.be/id848Ww1YLo?si=uoiFicM0MMX_7RBy", "trailer_thumbnail": "https://img.youtube.com/vi/id848Ww1YLo/maxresdefault.jpg", "mood": "Sweaty, immersive survival with huge emotional payoff.", "subtitles": ["English", "Hindi", "Malayalam"], "releaseDate": "2024-02-22", "trendingBadge": "Survival Favorite", "heroTag": "Friendship under pressure", "whyRecommended": "Because grounded thrills with heart linger with you.", "palette": {"primary": "#3b82f6", "secondary": "#1e3a8a", "accent": "#bfdbfe"}, "comingSoon": False},
    {"slug": "interstellar", "title": "Interstellar", "language": ["English"], "genre": ["Sci-Fi", "Adventure", "Drama"], "duration": "2h 49m", "runtimeMinutes": 169, "rating": 9.2, "imdbScore": 8.7, "rottenTomatoes": 73, "certificate": "UA", "storyline": "A desperate mission through a wormhole becomes a deeply human meditation on love, time, and survival.", "cast": [("Matthew McConaughey", "Cooper"), ("Anne Hathaway", "Brand"), ("Jessica Chastain", "Murph")], "trailer_watch_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E", "mood": "Cosmic awe with intimate emotional gravity.", "subtitles": ["English"], "releaseDate": "2014-11-07", "trendingBadge": "IMAX Legend", "heroTag": "Time, space, and love", "whyRecommended": "Because giant-format sci-fi belongs at the top of your list.", "palette": {"primary": "#60a5fa", "secondary": "#1e293b", "accent": "#e0f2fe"}, "comingSoon": False},
    {"slug": "oppenheimer", "title": "Oppenheimer", "language": ["English"], "genre": ["Drama", "Biography", "Thriller"], "duration": "3h 0m", "runtimeMinutes": 180, "rating": 9.0, "imdbScore": 8.3, "rottenTomatoes": 93, "certificate": "A", "storyline": "A brilliant physicist races toward creation while being consumed by the consequence of power.", "cast": [("Cillian Murphy", "J. Robert Oppenheimer"), ("Emily Blunt", "Kitty Oppenheimer"), ("Robert Downey Jr.", "Lewis Strauss")], "trailer_watch_url": "https://www.youtube.com/watch?v=uYPbbksJxIg", "mood": "Tense, atmospheric, and intellectually overwhelming.", "subtitles": ["English"], "releaseDate": "2023-07-21", "trendingBadge": "Awards Giant", "heroTag": "Power and fallout", "whyRecommended": "Because prestige event cinema deserves a prime slot.", "palette": {"primary": "#fb923c", "secondary": "#7f1d1d", "accent": "#fdba74"}, "comingSoon": False},
    {"slug": "dune-part-two", "title": "Dune: Part Two", "language": ["English"], "genre": ["Sci-Fi", "Adventure"], "duration": "2h 46m", "runtimeMinutes": 166, "rating": 9.1, "imdbScore": 8.5, "rottenTomatoes": 92, "certificate": "UA", "storyline": "Paul Atreides steps into prophecy, vengeance, and empire on a vast desert battlefield.", "cast": [("Timothée Chalamet", "Paul Atreides"), ("Zendaya", "Chani"), ("Rebecca Ferguson", "Lady Jessica")], "trailer_watch_url": "https://www.youtube.com/watch?v=Way9Dexny3w", "mood": "Monumental desert sci-fi with immaculate scale.", "subtitles": ["English"], "releaseDate": "2024-03-01", "trendingBadge": "Sci-Fi Pinnacle", "heroTag": "Prophecy forged in sand", "whyRecommended": "Because IMAX-scale sci-fi is absolutely your thing.", "palette": {"primary": "#f59e0b", "secondary": "#78350f", "accent": "#fde68a"}, "comingSoon": False},
    {"slug": "the-batman", "title": "The Batman", "language": ["English"], "genre": ["Action", "Crime", "Mystery"], "duration": "2h 56m", "runtimeMinutes": 176, "rating": 8.7, "imdbScore": 7.8, "rottenTomatoes": 85, "certificate": "UA", "storyline": "A younger, angrier Batman pursues a serial killer through a rain-soaked city of corruption.", "cast": [("Robert Pattinson", "Bruce Wayne"), ("Zoë Kravitz", "Selina Kyle"), ("Paul Dano", "Riddler")], "trailer_watch_url": "https://www.youtube.com/watch?v=mqqft2x_Aa4", "mood": "Noir dread, rain, and bruised detective energy.", "subtitles": ["English"], "releaseDate": "2022-03-04", "trendingBadge": "Gotham Noir", "heroTag": "Detective vengeance in the rain", "whyRecommended": "Because dark, atmospheric superhero stories fit your mood.", "palette": {"primary": "#dc2626", "secondary": "#111827", "accent": "#fecaca"}, "comingSoon": False},
    {"slug": "john-wick-4", "title": "John Wick: Chapter 4", "language": ["English"], "genre": ["Action", "Thriller"], "duration": "2h 49m", "runtimeMinutes": 169, "rating": 8.8, "imdbScore": 7.7, "rottenTomatoes": 94, "certificate": "A", "storyline": "The legendary assassin fights through ornate cities and escalating ritual violence for one final chance at freedom.", "cast": [("Keanu Reeves", "John Wick"), ("Donnie Yen", "Caine"), ("Bill Skarsgård", "Marquis")], "trailer_watch_url": "https://www.youtube.com/watch?v=qEVUtrk8_B4", "mood": "Elegant, relentless action choreography.", "subtitles": ["English"], "releaseDate": "2023-03-24", "trendingBadge": "Action Benchmark", "heroTag": "The table strikes back", "whyRecommended": "Because precision action filmmaking always wins.", "palette": {"primary": "#f43f5e", "secondary": "#111827", "accent": "#fda4af"}, "comingSoon": False},
    {"slug": "avengers-endgame", "title": "Avengers: Endgame", "language": ["English"], "genre": ["Action", "Sci-Fi", "Adventure"], "duration": "3h 1m", "runtimeMinutes": 181, "rating": 8.9, "imdbScore": 8.4, "rottenTomatoes": 94, "certificate": "UA", "storyline": "Earth's mightiest heroes make one final, time-bending stand to undo catastrophe.", "cast": [("Robert Downey Jr.", "Tony Stark"), ("Chris Evans", "Steve Rogers"), ("Scarlett Johansson", "Natasha Romanoff")], "trailer_watch_url": "https://www.youtube.com/watch?v=TcMBFSGVi1c", "mood": "Triumphant closure built for communal cheering.", "subtitles": ["English"], "releaseDate": "2019-04-26", "trendingBadge": "Marvel Event", "heroTag": "The last stand", "whyRecommended": "Because blockbuster finales still hit hardest in a crowd.", "palette": {"primary": "#6366f1", "secondary": "#312e81", "accent": "#c7d2fe"}, "comingSoon": False},
    {"slug": "spider-man-no-way-home", "title": "Spider-Man: No Way Home", "language": ["English"], "genre": ["Action", "Sci-Fi", "Adventure"], "duration": "2h 28m", "runtimeMinutes": 148, "rating": 8.8, "imdbScore": 8.2, "rottenTomatoes": 93, "certificate": "UA", "storyline": "Peter Parker's identity crisis fractures the multiverse and summons legacy heroes and villains alike.", "cast": [("Tom Holland", "Peter Parker"), ("Zendaya", "MJ"), ("Benedict Cumberbatch", "Doctor Strange")], "trailer_watch_url": "https://www.youtube.com/watch?v=JfVOs4VSpmA", "mood": "Nostalgic, emotional, and wildly crowd-pleasing.", "subtitles": ["English"], "releaseDate": "2021-12-17", "trendingBadge": "Multiverse Hit", "heroTag": "Webs across universes", "whyRecommended": "Because nostalgia and spectacle are a powerful combo.", "palette": {"primary": "#ef4444", "secondary": "#1d4ed8", "accent": "#bfdbfe"}, "comingSoon": False},
    {"slug": "inception", "title": "Inception", "language": ["English"], "genre": ["Sci-Fi", "Thriller", "Action"], "duration": "2h 28m", "runtimeMinutes": 148, "rating": 9.0, "imdbScore": 8.8, "rottenTomatoes": 87, "certificate": "UA", "storyline": "A dream thief attempts the impossible: planting an idea deep enough to change a future.", "cast": [("Leonardo DiCaprio", "Cobb"), ("Joseph Gordon-Levitt", "Arthur"), ("Elliot Page", "Ariadne")], "trailer_watch_url": "https://www.youtube.com/watch?v=YoHD9XEInc0", "mood": "Mind-bending and surgically cool.", "subtitles": ["English"], "releaseDate": "2010-07-16", "trendingBadge": "Mind-Bender", "heroTag": "Dreams inside dreams", "whyRecommended": "Because puzzle-box thrillers keep rewarding repeat watches.", "palette": {"primary": "#2563eb", "secondary": "#0f172a", "accent": "#93c5fd"}, "comingSoon": False},
    {"slug": "top-gun-maverick", "title": "Top Gun: Maverick", "language": ["English"], "genre": ["Action", "Drama"], "duration": "2h 11m", "runtimeMinutes": 131, "rating": 8.8, "imdbScore": 8.2, "rottenTomatoes": 96, "certificate": "UA", "storyline": "A legendary pilot returns to train a new class for a mission that demands impossible precision.", "cast": [("Tom Cruise", "Maverick"), ("Miles Teller", "Rooster"), ("Jennifer Connelly", "Penny")], "trailer_watch_url": "https://www.youtube.com/watch?v=giXco2jaZ_4", "mood": "Propulsive, emotional, and physically exhilarating.", "subtitles": ["English"], "releaseDate": "2022-05-27", "trendingBadge": "Aerial Triumph", "heroTag": "Altitude with heart", "whyRecommended": "Because practical-action spectacle is unbeatable in cinemas.", "palette": {"primary": "#38bdf8", "secondary": "#1d4ed8", "accent": "#bae6fd"}, "comingSoon": False},
    {"slug": "inside-out-2", "title": "Inside Out 2", "language": ["English"], "genre": ["Animation", "Family", "Comedy"], "duration": "1h 36m", "runtimeMinutes": 96, "rating": 8.4, "imdbScore": 7.8, "rottenTomatoes": 91, "certificate": "U", "storyline": "Teenage Riley's emotional headquarters gets a chaotic new upgrade when adolescence arrives.", "cast": [("Amy Poehler", "Joy"), ("Maya Hawke", "Anxiety"), ("Kensington Tallman", "Riley")], "trailer_watch_url": "https://www.youtube.com/watch?v=LEjhY15eCx0", "mood": "Bright, emotional, and family-friendly without losing depth.", "subtitles": ["English"], "releaseDate": "2024-06-14", "trendingBadge": "Family Smash", "heroTag": "Feelings level up", "whyRecommended": "Because big-hearted animation is a great all-ages pick.", "palette": {"primary": "#f472b6", "secondary": "#8b5cf6", "accent": "#fbcfe8"}, "comingSoon": False},
    {"slug": "coco", "title": "Coco", "language": ["English"], "genre": ["Animation", "Family", "Fantasy"], "duration": "1h 45m", "runtimeMinutes": 105, "rating": 8.7, "imdbScore": 8.4, "rottenTomatoes": 97, "certificate": "U", "storyline": "A music-loving child journeys into the Land of the Dead and rediscovers his family's forgotten story.", "cast": [("Anthony Gonzalez", "Miguel"), ("Gael García Bernal", "Héctor"), ("Benjamin Bratt", "Ernesto de la Cruz")], "trailer_watch_url": "https://www.youtube.com/watch?v=Rvr68u6k5sI", "mood": "Color-drenched, musical, and deeply moving.", "subtitles": ["English"], "releaseDate": "2017-11-22", "trendingBadge": "Family Classic", "heroTag": "Music across generations", "whyRecommended": "Because emotional animation always plays beautifully with families.", "palette": {"primary": "#f97316", "secondary": "#a21caf", "accent": "#fdba74"}, "comingSoon": False},
    {"slug": "a-quiet-place-day-one", "title": "A Quiet Place: Day One", "language": ["English"], "genre": ["Horror", "Thriller"], "duration": "1h 39m", "runtimeMinutes": 99, "rating": 7.9, "imdbScore": 6.8, "rottenTomatoes": 86, "certificate": "A", "storyline": "New York collapses into silence as the first alien attack rewrites every instinct for survival.", "cast": [("Lupita Nyong'o", "Sam"), ("Joseph Quinn", "Eric"), ("Alex Wolff", "Reuben")], "trailer_watch_url": "https://www.youtube.com/watch?v=YPY7J-flzE8", "mood": "Claustrophobic suspense with citywide dread.", "subtitles": ["English"], "releaseDate": "2024-06-28", "trendingBadge": "Horror Tension", "heroTag": "Silence becomes survival", "whyRecommended": "Because tight theatrical tension is best shared in a dark room.", "palette": {"primary": "#94a3b8", "secondary": "#111827", "accent": "#e2e8f0"}, "comingSoon": False},
    {"slug": "saiyaar", "title": "Saiyaara", "language": ["Hindi"], "genre": ["Romance", "Drama"], "duration": "2h 18m", "runtimeMinutes": 138, "rating": 8.1, "imdbScore": 7.3, "rottenTomatoes": 79, "certificate": "UA", "storyline": "A sweeping modern romance unfolds through music, longing, and impossible timing.", "cast": [("Ahaan Panday", "Krish"), ("Aneet Padda", "Misha"), ("Varun Badola", "Arjun")], "trailer_watch_url": "https://www.youtube.com/watch?v=9r-tT5IN0vg", "mood": "Dreamy romance with glossy musical heartbreak.", "subtitles": ["English", "Hindi"], "releaseDate": "2026-08-14", "trendingBadge": "Coming Soon Romance", "heroTag": "Love under city lights", "whyRecommended": "Because big-screen romance is back in your rotation.", "palette": {"primary": "#fb7185", "secondary": "#7c3aed", "accent": "#fbcfe8"}, "comingSoon": True},
    {"slug": "dhurandhar", "title": "Dhurandhar", "language": ["Hindi"], "genre": ["Action", "Thriller"], "duration": "2h 32m", "runtimeMinutes": 152, "rating": 8.0, "imdbScore": 7.1, "rottenTomatoes": 78, "certificate": "UA", "storyline": "A high-voltage action setup builds around power, scale, and a star-driven theatrical reveal.", "cast": [("Ranveer Singh", "Lead"), ("Sanjay Dutt", "Lead Antagonist"), ("R. Madhavan", "Strategist")], "trailer_watch_url": "https://www.youtube.com/watch?v=NHk7scrb_9I", "mood": "Explosive mass-action energy with swagger and menace.", "subtitles": ["English", "Hindi"], "releaseDate": "2026-12-05", "trendingBadge": "Action Event Incoming", "heroTag": "Power play on a giant canvas", "whyRecommended": "Because larger-than-life theatrical action is a strong match for this app.", "palette": {"primary": "#f97316", "secondary": "#431407", "accent": "#fdba74"}, "comingSoon": True},
    {"slug": "war-2", "title": "War 2", "language": ["Hindi", "Telugu"], "genre": ["Action", "Spy Thriller"], "duration": "2h 40m", "runtimeMinutes": 160, "rating": 8.5, "imdbScore": 7.4, "rottenTomatoes": 80, "certificate": "UA", "storyline": "The spy universe escalates into a larger conflict packed with betrayal, speed, and larger-than-life combat.", "cast": [("Hrithik Roshan", "Kabir"), ("N. T. Rama Rao Jr.", "Agent Vikram"), ("Kiara Advani", "Kavya")], "trailer_watch_url": "https://www.youtube.com/watch?v=3x77q40hATw", "mood": "Franchise scale, polished espionage, and crossover hype.", "subtitles": ["English", "Hindi"], "releaseDate": "2026-11-14", "trendingBadge": "Spy Universe Incoming", "heroTag": "Agents collide again", "whyRecommended": "Because you enjoy premium-format action franchises.", "palette": {"primary": "#f59e0b", "secondary": "#1f2937", "accent": "#fde68a"}, "comingSoon": True},
    {"slug": "the-batman-part-ii", "title": "The Batman Part II", "language": ["English"], "genre": ["Action", "Crime", "Mystery"], "duration": "2h 50m", "runtimeMinutes": 170, "rating": 8.7, "imdbScore": 7.8, "rottenTomatoes": 85, "certificate": "UA", "storyline": "Gotham's nightmare deepens as a more seasoned Batman faces fresh corruption and obsession.", "cast": [("Robert Pattinson", "Bruce Wayne"), ("Zoë Kravitz", "Selina Kyle"), ("Andy Serkis", "Alfred")], "trailer_watch_url": "https://www.youtube.com/watch?v=T7_zMl_ZhdQ", "trailer_thumbnail": "https://img.youtube.com/vi/T7_zMl_ZhdQ/maxresdefault.jpg", "mood": "Gothic, stormy, and thick with noir menace.", "subtitles": ["English"], "releaseDate": "2026-10-02", "trendingBadge": "Coming Soon Noir", "heroTag": "Gotham gets darker", "whyRecommended": "Because grim detective superhero cinema suits your taste.", "palette": {"primary": "#b91c1c", "secondary": "#111827", "accent": "#fecaca"}, "comingSoon": True},
    {"slug": "avatar-fire-and-ash", "title": "Avatar: Fire and Ash", "language": ["English"], "genre": ["Sci-Fi", "Adventure"], "duration": "3h 5m", "runtimeMinutes": 185, "rating": 8.8, "imdbScore": 7.7, "rottenTomatoes": 84, "certificate": "UA", "storyline": "Pandora's beauty turns more volatile as new clans, landscapes, and warfare reshape the saga.", "cast": [("Sam Worthington", "Jake Sully"), ("Zoe Saldaña", "Neytiri"), ("Sigourney Weaver", "Kiri")], "trailer_watch_url": "https://www.youtube.com/watch?v=8Wk6QmWJ4V4", "mood": "Glowing ecosystems, warfare, and colossal scale.", "subtitles": ["English"], "releaseDate": "2026-12-18", "trendingBadge": "Future IMAX Event", "heroTag": "Pandora in flames", "whyRecommended": "Because large-format worldbuilding keeps drawing you in.", "palette": {"primary": "#22d3ee", "secondary": "#155e75", "accent": "#a5f3fc"}, "comingSoon": True},
    {"slug": "charlie-777-reissue", "title": "777 Charlie Reissue", "language": ["Kannada", "Hindi"], "genre": ["Family", "Drama"], "duration": "2h 44m", "runtimeMinutes": 164, "rating": 8.2, "imdbScore": 8.7, "rottenTomatoes": 94, "certificate": "U", "storyline": "A special theatrical reissue for one of the most loved emotional road stories in recent Indian cinema.", "cast": [("Rakshit Shetty", "Dharma"), ("Sangeetha Sringeri", "Devika"), ("Raj B. Shetty", "Dr. Ashwin")], "trailer_watch_url": "https://www.youtube.com/watch?v=vK4v2M4lreA", "mood": "Warm, emotional, and perfect for family bookings.", "subtitles": ["English", "Hindi", "Kannada"], "releaseDate": "2026-05-30", "trendingBadge": "Special Reissue", "heroTag": "Beloved road journey returns", "whyRecommended": "Because family movies with heart deserve another run.", "palette": {"primary": "#14b8a6", "secondary": "#0f766e", "accent": "#99f6e4"}, "comingSoon": True},
    {"slug": "premalu-2", "title": "Premalu 2", "language": ["Malayalam", "Hindi"], "genre": ["Romance", "Comedy"], "duration": "2h 20m", "runtimeMinutes": 140, "rating": 8.2, "imdbScore": 7.6, "rottenTomatoes": 82, "certificate": "U", "storyline": "A beloved rom-com world expands with more awkward charm, urban energy, and sweet misunderstandings.", "cast": [("Naslen", "Sachin"), ("Mamitha Baiju", "Reenu"), ("Sangeeth Prathap", "Amal Davis")], "trailer_watch_url": "https://www.youtube.com/watch?v=ELtVYbM7w2o", "mood": "Bubbly romance with metropolitan sparkle.", "subtitles": ["English", "Hindi", "Malayalam"], "releaseDate": "2026-09-25", "trendingBadge": "Rom-Com Return", "heroTag": "Hyderabad love story continues", "whyRecommended": "Because feel-good romance is always welcome.", "palette": {"primary": "#f472b6", "secondary": "#9333ea", "accent": "#fbcfe8"}, "comingSoon": True},
]


def _categories_from_blueprint(blueprint: dict) -> list[str]:
    categories = {"Recommended", "Trending Now"}
    genres = set(blueprint["genre"])
    if "Sci-Fi" in genres:
        categories.add("Sci-Fi")
    if "Action" in genres:
        categories.add("Action")
    if "Romance" in genres:
        categories.add("Romance")
    if "Horror" in genres:
        categories.add("Horror")
    if "Family" in genres or "Animation" in genres:
        categories.add("Family Movies")
    if blueprint["comingSoon"]:
        categories.add("Coming Soon")
    if blueprint["imdbScore"] >= 8.0:
        categories.add("Top Rated")
    if any(genre in genres for genre in ["Sci-Fi", "Action", "Adventure", "Epic"]):
        categories.add("IMAX Experience")
    return sorted(categories)


def _build_catalog_entry(blueprint: dict, all_titles: list[str]) -> dict:
    assets = asset_bundle(blueprint["slug"])
    cast_list = [
        build_actor(name, role, blueprint["title"], all_titles, index * 7 + len(name))
        for index, (name, role) in enumerate(blueprint["cast"])
    ]
    return {
        "title": blueprint["title"],
        "slug": blueprint["slug"],
        "genre": blueprint["genre"],
        "duration": blueprint["duration"],
        "runtimeMinutes": blueprint["runtimeMinutes"],
        "rating": blueprint["rating"],
        "imdbScore": blueprint["imdbScore"],
        "rottenTomatoes": blueprint["rottenTomatoes"],
        "certificate": blueprint["certificate"],
        "storyline": blueprint["storyline"],
        "cast": cast_list,
        "castImages": [item["image"] for item in cast_list],
        "poster": assets["poster"],
        "backdrop": assets["backdrop"],
        "logo": assets["logo"],
        "gallery": assets["gallery"],
        "trailer_watch_url": blueprint["trailer_watch_url"],
        "trailer_thumbnail": blueprint.get("trailer_thumbnail"),
        "trailer_variants": deepcopy(blueprint.get("trailer_variants", [])),
        "is_placeholder": blueprint.get("is_placeholder", False),
        "mood": blueprint["mood"],
        "languages": blueprint["language"],
        "subtitles": blueprint["subtitles"],
        "releaseDate": blueprint["releaseDate"],
        "trendingBadge": blueprint["trendingBadge"],
        "heroTag": blueprint["heroTag"],
        "whyRecommended": blueprint["whyRecommended"],
        "comingSoon": blueprint["comingSoon"],
        "palette": blueprint["palette"],
        "categories": _categories_from_blueprint(blueprint),
    }


ALL_CATALOG_TITLES = [item["title"] for item in MOVIE_BLUEPRINTS]
MOVIE_CATALOG = {
    normalize_catalog_key(item["title"]): _build_catalog_entry(item, ALL_CATALOG_TITLES)
    for item in MOVIE_BLUEPRINTS
}


def catalog_movie_rows() -> list[dict]:
    return [
        {
            "title": item["title"].upper(),
            "language": ", ".join(language.lower() for language in item["language"]),
            "releaseDate": item["releaseDate"],
        }
        for item in MOVIE_BLUEPRINTS
    ]


def _fallback_metadata(movie_name: str):
    slug = normalize_catalog_key(movie_name)
    assets = asset_bundle(slug)
    return {
        "title": movie_name.title(),
        "slug": slug,
        "genre": ["Drama", "Event Cinema"],
        "duration": "2h 18m",
        "runtimeMinutes": 138,
        "rating": 8.0,
        "imdbScore": 7.5,
        "rottenTomatoes": 81,
        "certificate": "UA",
        "storyline": f"{movie_name.title()} is presented as a premium theatrical event with emotional scale, polished visuals, and strong booking intent.",
        "cast": [build_actor("Lead Star", f"{movie_name.title()} Lead", movie_name.title(), ALL_CATALOG_TITLES, 12)],
        "castImages": [actor_image_path("Lead Star")],
        "poster": assets["poster"],
        "backdrop": assets["backdrop"],
        "logo": assets["logo"],
        "gallery": assets["gallery"],
        "trailer_watch_url": DEFAULT_TRAILER_WATCH,
        "mood": "A premium theatrical event with cinematic momentum.",
        "languages": ["Hindi"],
        "subtitles": ["English", "Hindi"],
        "releaseDate": date.today().isoformat(),
        "trendingBadge": "Now Booking",
        "heroTag": "Premium theatrical event",
        "whyRecommended": "Because your recent browsing leans toward theatrical event films.",
        "comingSoon": False,
        "palette": {"primary": "#38bdf8", "secondary": "#1e293b", "accent": "#bae6fd"},
        "categories": ["Recommended", "Trending Now"],
    }


def build_movie_metadata(movie_name: str):
    key = normalize_catalog_key(movie_name)
    base = deepcopy(MOVIE_CATALOG.get(key, _fallback_metadata(movie_name)))
    base["trailer_watch_url"] = trailer_watch_url(base.get("trailer_watch_url", DEFAULT_TRAILER_WATCH))
    base["trailer_url"] = youtube_embed(base["trailer_watch_url"])
    base["trailer_thumbnail"] = base.get("trailer_thumbnail") or youtube_thumbnail(base["trailer_watch_url"])
    base["trailer_variants"] = deepcopy(base.get("trailer_variants", []))
    base["is_placeholder"] = bool(base.get("is_placeholder", False))
    base["trailer_available"] = bool(base["trailer_url"]) and not base["is_placeholder"]
    base["trailer_cta"] = "Watch Trailer" if base["trailer_available"] else "View Trailer Updates"
    base["foodCombos"] = deepcopy(FOOD_COMBOS)
    base["coupons"] = deepcopy(COUPONS)
    base["paymentMethods"] = deepcopy(PAYMENT_METHODS)
    return base


def infer_screen_formats(screen_name: str):
    name = screen_name.lower()
    formats = []
    if "imax" in name:
        formats.append("IMAX")
    if "atmos" in name or "dolby" in name:
        formats.append("Dolby Atmos")
    if "4dx" in name:
        formats.append("4DX")
    if "recliner" in name:
        formats.append("Recliner")
    if "laser" in name:
        formats.append("Laser Projection")
    if not formats:
        formats.append("Laser Projection")
    return formats


def price_modifiers(screen_name: str):
    name = screen_name.lower()
    return {
        "weekend": 1.18,
        "premiumSeat": 1.25 if "recliner" in name else 1.12,
        "imax": 1.35 if "imax" in name else 1.1,
    }


def infer_chain(theater_name: str):
    for chain in THEATER_PHOTOS:
        if theater_name.lower().startswith(chain.lower()):
            return chain
    return "PVR"


def theater_distance(theater_id: int):
    return round(1.4 + ((theater_id * 1.37) % 7.2), 1)


def theater_area(city: str, theater_id: int):
    areas = CITY_AREAS.get(city, ["City Centre"])
    return areas[theater_id % len(areas)]


def build_theater_profile(theater, screens: list, shows: list):
    chain = infer_chain(theater.name)
    formats = sorted({fmt for screen in screens for fmt in infer_screen_formats(screen.screen_name)})
    return {
        "id": theater.id,
        "name": theater.name,
        "city": theater.city,
        "chain": chain,
        "screens": len(screens),
        "formats": formats,
        "seatCapacity": sum(screen.total_seats for screen in screens),
        "ratings": round(4.1 + ((theater.id % 7) * 0.1), 1),
        "location": theater_area(theater.city, theater.id),
        "distance": theater_distance(theater.id),
        "facilities": THEATER_FACILITIES.get(chain, ["Premium seating", "Quick food pickup", "Digital tickets"]),
        "showsCount": len(shows),
        "photo": THEATER_PHOTOS.get(chain, "/assets/theaters/pvr.svg"),
    }
