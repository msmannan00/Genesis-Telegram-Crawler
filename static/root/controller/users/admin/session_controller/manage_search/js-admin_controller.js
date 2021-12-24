!function(s){function e(s){return s instanceof Object&&Object.keys(s).length>0}s.fn.jsonViewer=function(l,a){return a=Object.assign({},{collapsed:!1,rootCollapsable:!0,withQuotes:!1,withLinks:!0},a),this.each(function(){var t=function s(l,a){var t="";if("string"==typeof l)l=l.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/'/g,"&apos;").replace(/"/g,"&quot;"),a.withLinks&&/^(https?:\/\/|ftps?:\/\/)?([a-z0-9%-]+\.){1,}([a-z0-9-]+)?(:(\d{1,5}))?(\/([a-z0-9\-._~:/?#[\]@!$&'()*+,;=%]+)?)?$/i.test(l)?t+='<a href="'+l+'" class="json-string" target="_blank">'+l+"</a>":t+='<span class="json-string">"'+(l=l.replace(/&quot;/g,"\\&quot;"))+'"</span>';else if("number"==typeof l)t+='<span class="json-literal">'+l+"</span>";else if("boolean"==typeof l)t+='<span class="json-literal">'+l+"</span>";else if(null===l)t+='<span class="json-literal">null</span>';else if(l instanceof Array)if(l.length>0){t+='[<ol class="json-array">';for(var n=0;n<l.length;++n)t+="<li>",e(l[n])&&(t+='<a href class="json-toggle"></a>'),t+=s(l[n],a),n<l.length-1&&(t+=","),t+="</li>";t+="</ol>]"}else t+="[]";else if("object"==typeof l){var o=Object.keys(l).length;if(o>0){for(var i in t+='{<ul class="json-dict">',l)if(Object.prototype.hasOwnProperty.call(l,i)){t+="<li>";var r=a.withQuotes?'<span class="json-string">"'+i+'"</span>':i;e(l[i])?t+='<a href class="json-toggle">'+r+"</a>":t+=r,t+=": "+s(l[i],a),--o>0&&(t+=","),t+="</li>"}t+="</ul>}"}else t+="{}"}return t}(l,a);a.rootCollapsable&&e(l)&&(t='<a href class="json-toggle"></a>'+t),s(this).html(t),s(this).addClass("json-document"),s(this).off("click"),s(this).on("click","a.json-toggle",function(){var e=s(this).toggleClass("collapsed").siblings("ul.json-dict, ol.json-array");if(e.toggle(),e.is(":visible"))e.siblings(".json-placeholder").remove();else{var l=e.children("li").length,a=l+(l>1?" items":" item");e.after('<a href class="json-placeholder">'+a+"</a>")}return!1}),s(this).on("click","a.json-placeholder",function(){return s(this).siblings("a.json-toggle").click(),!1}),1==a.collapsed&&s(this).find("a.json-toggle").click()})}}(jQuery);
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
      let response = JSON.parse(replaced)

      let m_html = ""
      m_html += "<div style='padding: 5px'>"
      let i = 0, l = response.length;
      for (; i < l; i++) {
          m_html += "<div style='border: 1px solid #e6e6e6;border-radius: 7px;background: #f8f8f8'>"
          m_html += "<div style='font-size: 13px; color: darkgreen;padding-left: 15px;padding-top: 15px;padding-bottom: 5px'>Channel URL : <b>" + response[i]['_source']['m_channel_url'] + "</b></div>"
          m_html += "<div style='font-size: 13px; color: darkgreen;padding-left: 15px;padding-top: -10px;padding-bottom: 5px'>Content Category : <b>" + response[i]['_source']['m_category'] + "</b></div>"
          m_html += "<hr>"
          m_html += "<div style='font-size: 15px; color: gray;padding-left: 15px;margin-top: -10px;padding-bottom: 10px'>" + response[i]['_source']['text'] + "</div>"
          m_html += "</div><br>"

          if (i>=6){
              break
          }
      }
      m_html += "</div>"
      document.getElementById(DOM.S_DISPLAY_SEARCH).innerHTML = m_html
      document.getElementById('json-renderer').style.display = "block";

      $('#json-renderer').jsonViewer(response);

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
