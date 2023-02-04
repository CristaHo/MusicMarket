

<p>Search by:</p>
    <select name="songs" id="song-select">
        <option value="">--Please choose an option--</option>
        <option value="artist">Artist</option>
        <option value="song">Song</option>
        <option value="genre">Genre</option>
        <option value="date">Darrot</option>
        
    </select> <br>

{% for song in results %}
<li> {{ song.artist }} - {{ song.song_name }} 
{% endfor %}
</ul>
<hr>
<a href="/">Takaisin</a>
    