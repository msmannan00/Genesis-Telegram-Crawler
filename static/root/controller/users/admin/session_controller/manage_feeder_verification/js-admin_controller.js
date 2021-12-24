class admin_controller {
  ajax_request(p_data, p_command) {
    $.ajax({
        url: '/manage-feeder-verification',
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

}

let m_admin_controller = new admin_controller();
function invoke_trigger(p_command) {
    if(p_command === COMMANDS.S_SUBMIT_VERIFICATION){
      let m_feeder_verification_token = document.getElementById(DOM.S_FEEDER_VERIFICATION).value

      let parsedJSON = JSON.parse('{"' + KEY.S_FEEDER_VERIFICATION + '":"' + m_feeder_verification_token + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_VERIFICATION + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
      window.close();
    }
    if(p_command === COMMANDS.S_SUBMIT_TIMER){
        let m_time = 30
        let m_interval = setInterval(function () {
            m_time = m_time-1
            let seconds = m_time;

            document.getElementById(DOM.S_FEEDER_TIMER).innerHTML = seconds + " seconds to expire";

            if (parseInt(m_time) < 0) {
                clearInterval(m_interval);
                window.close();
                close()
            }
        }, 1000);
    }
}
