$(document).ready(setup);

  function setup(){
    $(".fa-trash").click(deleteinput)
    // fa-trash.onMouseClick

  }


function deleteinput(){
    var usertext = $(this).parent().text()
    console.log(usertext)
    var category = $(this).parent().parent().attr('class')



    var url = '/deleteinput'
    var data = {"category":category,"input":usertext }
    var settings = {"type":"POST", "data":data}



    $.ajax(url, settings)

    $(this).parent().remove()

}
