<br>
<table>
    <tr>
        <td>Author</td>
        <td>Name</td>
        <td>Last Updated</td>
    </tr>
    {% for repo in site.data.repos %}
    <tr>
        <td>{{ repo.Author }}</td>
        <td>
            <!--suppress HtmlUnknownTarget -->
            <a rel="repo"
              href="{{ repo.URL }}"
              title="{{ repo.Name }}">
                {{ repo.Name }}
            </a>
        </td>
        <td>{{ repo.LastUpdated }}</td>
    </tr>
    {% endfor %}
</table>