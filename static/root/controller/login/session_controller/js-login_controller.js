class login_controller {
  ajax_request(p_data) {
    $.ajax({
        url: '/login',
        data: p_data,
        type: 'GET',
        success: function(response){
            console.log(response);
            if (response === CALLBACK_MESSAGES.S_SUCCESS){
                window.location.href = "/";
            }else {
                document.getElementById(DOM.S_ERROR).innerText = response
            }
		},
        error: function(error){
            console.log(error);
        }
    });
  }
}

let m_login_controller = new login_controller();
function invoke_trigger(p_command) {
    if (p_command === COMMANDS.S_VERIFY_LOGIN_REQUEST){

      let m_username = document.getElementById(DOM.S_USERNAME).value
      let m_password = document.getElementById(DOM.S_PASSWORD).value
      let parsedJSON = JSON.parse('{"' + DOM.S_USERNAME + '":"' + m_username + '","' + DOM.S_PASSWORD + '":"' + m_password + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_VERIFY_LOGIN_REQUEST + '"}')
      m_login_controller.ajax_request(parsedJSON)
    }
}
