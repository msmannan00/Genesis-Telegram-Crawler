class admin_controller {
  ajax_request(p_data, p_command) {
    $.ajax({
        url: '/manage-feeder',
        data: p_data,
        type: 'GET',
        success: function(response){
            console.log(response);
            m_admin_controller.on_ajax_post(p_command, response)
		},
        error: function(error){
            console.log(error);
            m_admin_controller.on_ajax_post(p_command, error)
        }
    });
  }

  on_ajax_post(p_command, p_message){

     if(p_command === COMMANDS.S_SUBMIT_INSERT){
            document.getElementById(DOM.S_PANEL_INSERT).style.display = "none";
            document.getElementById(DOM.S_PANEL_DELETE).style.display = "none";
            document.getElementById(DOM.S_PANEL_VIEW).style.display = "none";
            document.getElementById(DOM.S_RESPONSE).style.display = "none";
            document.getElementById(DOM.S_PANEL_VERIFICATION).style.display = "none";

            document.getElementById(DOM.S_FEEDER_INSERT).value = ""
            document.getElementById(DOM.S_FEEDER_PHONE).value = ""
            document.getElementById(DOM.S_RESPONSE_CONTAINER).style.display = "block";
            document.getElementById(DOM.S_RESPONSE).innerText = p_message
            document.getElementById(DOM.S_RESPONSE).style.display = "block";
            document.getElementById(DOM.S_PANEL_INSERT).style.display = "block";


            if (p_message.includes("success")){
                window.open("./manage-feeder-verification","_blank")
            }
     }
     if(p_command === COMMANDS.S_SUBMIT_DELETE){
         document.getElementById(DOM.S_FEEDER_DELETE).value = ""
         document.getElementById(DOM.S_RESPONSE_CONTAINER).style.display = "block";
         document.getElementById(DOM.S_RESPONSE).innerText = p_message
         document.getElementById(DOM.S_RESPONSE).style.display = "block";
     }
    if(p_command === COMMANDS.S_SUBMIT_VIEW){

        const m_json = JSON.parse(p_message);
        let m_html = "<table class=\"table\"> <thead> <tr> <th scope=\"col\">#</th> <th scope=\"col\">Channel URL</th> <th scope=\"col\">T-ID</th></tr></thead>"
        m_html += "<tbody>"
        let i = 0;
        for (const [key, value] of Object.entries(m_json)) {
            i = i+1
            m_html += "<tr>"
            m_html += "<th>" + (i) + "</th><td>"+key+"</td><td>"+value+"</td>"
            m_html += "</tr>"
        }

        m_html += "</tbody>"
        m_html += "</table>"
        document.getElementById(DOM.S_PANEL_VIEW).innerHTML = m_html;
     }
  }


  on_change_admin_view(p_command){
    document.getElementById(DOM.S_PANEL_INSERT).style.display = "none";
    document.getElementById(DOM.S_PANEL_DELETE).style.display = "none";
    document.getElementById(DOM.S_PANEL_VIEW).style.display = "none";
    document.getElementById(DOM.S_RESPONSE).style.display = "none";
    document.getElementById(DOM.S_PANEL_VERIFICATION).style.display = "none";


    if (p_command === COMMANDS.S_ON_INSERT){
        document.getElementById(DOM.S_PANEL_INSERT).style.display = "block";
    }
    else if (p_command === COMMANDS.S_ON_DELETE){
        document.getElementById(DOM.S_PANEL_DELETE).style.display = "block";
    }
    else if (p_command === COMMANDS.S_ON_VIEW){
        document.getElementById(DOM.S_PANEL_VIEW).style.display = "block";
    }
  }
}

let m_admin_controller = new admin_controller();
function invoke_trigger(p_command) {
    if (p_command === COMMANDS.S_ON_INSERT || p_command === COMMANDS.S_ON_DELETE || p_command === COMMANDS.S_ON_VIEW){
        m_admin_controller.on_change_admin_view(p_command)
    }
    if(p_command === COMMANDS.S_SUBMIT_INSERT){
      let m_feeder_name = document.getElementById(DOM.S_FEEDER_INSERT).value
      let m_feeder_phone = document.getElementById(DOM.S_FEEDER_PHONE).value

      let parsedJSON = JSON.parse('{"' + KEY.S_FEEDER_NAME + '":"' + m_feeder_name + '","' + KEY.S_FEEDER_PHONE + '":"' + m_feeder_phone + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_INSERT + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
    }
    if(p_command === COMMANDS.S_SUBMIT_DELETE){
      let m_feeder_name = document.getElementById(DOM.S_FEEDER_DELETE).value

      let parsedJSON = JSON.parse('{"' + KEY.S_FEEDER_NAME + '":"' + m_feeder_name + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_DELETE + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
    }
    if(p_command === COMMANDS.S_SUBMIT_VIEW || p_command === COMMANDS.S_ON_VIEW){
      let parsedJSON = JSON.parse('{"' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_VIEW + '"}')
      m_admin_controller.ajax_request(parsedJSON, COMMANDS.S_SUBMIT_VIEW)
    }
}
