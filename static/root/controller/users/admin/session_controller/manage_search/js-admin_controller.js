class admin_controller {
  ajax_request(p_data, p_command) {
    $.ajax({
        url: '/manage-search',
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
      const replaced = p_message.replaceAll(`'`, `"`);
      alert(replaced)
      let response = JSON.parse(replaced)

      let m_html = ""
      m_html += "<div style='padding: 5px'>"
      for (var i = 0, l = response.length; i < l; i++) {
          m_html += "<div style='border: 1px solid #e6e6e6;border-radius: 7px;background: #f8f8f8'>"
          m_html += "<div style='font-size: 13px; color: darkgreen;padding-left: 15px;padding-top: 15px;padding-bottom: 5px'>Channel URL : <b>" + response[i]['_source']['m_channel_url'] + "</b></div>"
          m_html += "<div style='font-size: 13px; color: darkgreen;padding-left: 15px;padding-top: -10px;padding-bottom: 5px'>Content Category : <b>" + response[i]['_source']['m_category'] + "</b></div>"
          m_html += "<hr>"
          m_html += "<div style='font-size: 15px; color: gray;padding-left: 15px;margin-top: -10px;padding-bottom: 10px'>" + response[i]['_source']['text'] + "</div>"
          m_html += "</div><br>"
      }
      m_html += "</div>"

      document.getElementById(DOM.S_DISPLAY_SEARCH).innerHTML = m_html
  }

}

let m_admin_controller = new admin_controller();
function invoke_trigger(p_command) {
    if(p_command === COMMANDS.S_SUBMIT_SEARCH){
      let m_query = document.getElementById(DOM.S_SUBMIT_SEARCH).value

      let parsedJSON = JSON.parse('{"' + KEY.S_SUBMIT_SEARCH + '":"' + m_query + '","' + KEY.S_COMMAND + '":"' + COMMANDS.S_SUBMIT_SEARCH + '"}')
      m_admin_controller.ajax_request(parsedJSON, p_command)
    }
}
