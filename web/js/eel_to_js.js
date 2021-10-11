// Передаем значения в Python для обработки и получения результата
function query_to_python()
{
	  eel.get_content_PY(read_command())
}


function read_command()
{
    let action = document.getElementById('action').value;
    let value = document.getElementById('command').value;

    return {
      'action': action,
      'value': value
    }
}


// Выводим полученную от Python информацию
eel.expose(output_to_html_JS);
function output_to_html_JS(data)
{		
	 document.getElementById('data').innerHTML = "<ul>" + data + "</ul>";
}


eel.expose(output_authors_to_html_JS);
function output_authors_to_html_JS(data, query)
{
    content = "По запросу ("+ query +") найдено:";
    content += "<div>Ключевые слова: <br><img src='words_cloud.png' style='width:100%'> </div>";
    console.log(data);
    table = "<table>";
    table += "<thead><tr><td>Автор</td><td>Кол-во публикаций</td></tr></thead>"
    table += "<tbody>";
    for (let keys in data) {
       // for (let key in data[keys]) {
            table += "<tr><td>" + data[keys][0] + "</td><td>" +  data[keys][1] + "</td></tr>" ;
       // }
    }
    table += "</tbody></table>";
    document.getElementById('all_nodes').innerHTML = "<ul style='padding-inline-start: 0px;'>" + table + "</ul>";
    document.getElementById('data').innerHTML = "<ul>" + content + "</ul>";
}


eel.expose(output_answers_results_to_html_JS);
function output_answers_results_to_html_JS(results)
{
    content = "</div>Ваши результаты:</div>";
    for (i=0; i<results.length; i++)
    {
        content += "<div class='results'>" + results[i][0] + " | <span class='" + results[i][2] + "'>" + results[i][1] + "</span></div>";
    }
     document.getElementById('data').innerHTML = "<ul>" + content + "</ul>";
}