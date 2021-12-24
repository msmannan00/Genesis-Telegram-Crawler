const COMMANDS = {
  S_ON_INSERT : 1,
  S_ON_DELETE : 2,
  S_ON_VIEW : 3,

  S_SUBMIT_INSERT : 4,
  S_SUBMIT_DELETE : 5,
  S_SUBMIT_VIEW : 6,
};

const CALLBACK = {
  VERIFICATION_CODE_SENT : "VERIFICATION_CODE_SENT"
};

const KEY = {
  S_FEEDER_NAME : 'p_feeder_name',
  S_FEEDER_PHONE : 'p_feeder_phone',
  S_COMMAND : 'p_command',
};

const DOM = {
  S_PANEL_INSERT : 'm_insert',
  S_PANEL_DELETE : 'm_delete',
  S_PANEL_VIEW : 'm_view',
  S_PANEL_VERIFICATION : 'm_verification',

  S_FEEDER_INSERT : 'p_feeder_url_insert',
  S_FEEDER_PHONE : 'p_feeder_url_phone',
  S_FEEDER_DELETE : 'p_feeder_url_delete',
  S_FEEDER_VERIFICATION : 'p_feeder_url_verification',

  S_RESPONSE_CONTAINER : 'm_view_display_container',
  S_RESPONSE : 'p_response'
};
