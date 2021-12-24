class admin_controller {
  ajax_request(p_data, p_command) {
    $.ajax({
        url: '/manage-user',
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
        document.getElementById(DOM.S_USERNAME_INSERT).value = ""
        document.getElementById(DOM.S_PASSWORD_INSERT).value = ""
        document.getElementById(DOM.S_RESPONSE_CONTAINER).style.display = "block";
        document.getElementById(DOM.S_RESPONSE).innerText = p_message
    }
    if(p_command === COMMANDS.S_SUBMIT_UPDATE){
        document.getElementById(DOM.S_USERNAME_UPDATE).value = ""
        document.getElementById(DOM.S_PASSWORD_UPDATE).value = ""
        document.getElementById(DOM.S_RESPONSE_CONTAINER).style.display = "block";
        document.getElementById(DOM.S_RESPONSE).innerText = p_message
    }
    if(p_command === COMMANDS.S_SUBMIT_DELETE){
        document.getElementById(DOM.S_USERNAME_DELETE).value = ""
        document.getElementById(DOM.S_RESPONSE_CONTAINER).style.display = "block";
        document.getElementById(DOM.S_RESPONSE).innerText = p_message
    }
    if(p_command === COMMANDS.S_SUBMIT_VIEW){
        let m_data = JSON.parse(p_message);
        let m_html = "<table class=\"table\"> <thead> <tr> <th scope=\"col\">#</th> <th scope=\"col\">Username</th> <th scope=\"col\">Password</th> <th scope=\"col\">Role</th> </tr></thead>"
        m_html += "<tbody>"
        for (let i = 0; i < m_data['m_data'].length; i++) {
            m_html += "<tr>"
                m_html += "<th>" + (i+1) + "</th><td>"+m_data['m_data'][i][0]+"</td><td>"+m_data['m_data'][i][1]+"</td><td>"+m_data['m_data'][i][2]+"</td>"
            m_html += "</tr>"
        }
        m_html += "</tbody>"
        m_html += "</table>"

        document.getElementById(DOM.S_PANEL_VIEW).innerHTML = m_html
    }
  }


  on_change_admin_view(p_command){

    document.getElementById(DOM.S_PANEL_INSERT).style.display = "none";
    document.getElementById(DOM.S_PANEL_UPDATE).style.display = "none";
    document.getElementById(DOM.S_PANEL_DELETE).style.display = "none";
    document.getElementById(DOM.S_PANEL_VIEW).style.display = "none";
    document.getElementById(DOM.S_RESPONSE_CONTAINER).style.display = "none";

    if (p_command === COMMANDS.S_ON_INSERT){
        document.getElementById(DOM.S_PANEL_INSERT).style.display = "block";
    }
    else if (p_command === COMMANDS.S_ON_UPDATE){
        document.getElementById(DOM.S_PANEL_UPDATE).style.display = "block";
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
    if (p_command === COMMANDS.S_ON_INSERT || p_command === COMMANDS.S_ON_UPDATE || p_command === COMMANDS.S_ON_DELETE || p_command === COMMANDS.S_ON_VIEW){
        m_admin_controller.on_change_admin_view(p_command)
    }
    if (p_command === COMMANDS.S_ON_VIEW){
        let parsedJSON = JSON.parse('{"' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_VIEW + '"}')
        m_admin_controller.ajax_request(parsedJSON, COMMANDS.S_SUBMIT_VIEW)
    }
    else if(p_command === COMMANDS.S_SUBMIT_INSERT){
      let m_username = document.getElementById(DOM.S_USERNAME_INSERT).value
      let m_password = document.getElementById(DOM.S_PASSWORD_INSERT).value
      let m_role = $('#p_role_insert input:radio:checked').val()

      let parsedJSON = JSON.parse('{"' + KEY.S_USERNAME + '":"' + m_username + '","' + KEY.S_PASSWORD + '":"' + m_password + '","' + KEY.S_ROLE + '":"' + m_role + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_INSERT + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
    }
    else if(p_command === COMMANDS.S_SUBMIT_UPDATE){
      let m_username = document.getElementById(DOM.S_USERNAME_UPDATE).value
      let m_password = document.getElementById(DOM.S_PASSWORD_UPDATE).value
      let m_role = $('#p_role_update input:radio:checked').val()

      let parsedJSON = JSON.parse('{"' + KEY.S_USERNAME + '":"' + m_username + '","' + KEY.S_PASSWORD + '":"' + m_password + '","' + KEY.S_ROLE + '":"' + m_role + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_UPDATE + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
    }
    else if(p_command === COMMANDS.S_SUBMIT_DELETE){
      let m_username = document.getElementById(DOM.S_USERNAME_DELETE).value

      let parsedJSON = JSON.parse('{"' + KEY.S_USERNAME + '":"' + m_username + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_DELETE + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
    }
}
