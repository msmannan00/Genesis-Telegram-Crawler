const COMMANDS = {
  S_ON_INSERT : 1,
  S_ON_UPDATE : 2,
  S_ON_DELETE : 3,
  S_ON_VIEW : 4,

  S_SUBMIT_INSERT : 5,
  S_SUBMIT_UPDATE : 6,
  S_SUBMIT_DELETE : 7,
  S_SUBMIT_VIEW : 8,
};

const KEY = {
  S_COMMAND : 'p_command',
  S_USERNAME : 'p_username',
  S_PASSWORD : 'p_password',
  S_ROLE : 'p_role'
};

const DOM = {
  S_PANEL_INSERT : 'm_insert',
  S_PANEL_UPDATE : 'm_update',
  S_PANEL_DELETE : 'm_remove',
  S_PANEL_VIEW : 'm_view',

  S_USERNAME_INSERT : 'p_username_insert',
  S_USERNAME_UPDATE : 'p_username_update',
  S_USERNAME_DELETE : 'p_username_delete',

  S_PASSWORD_INSERT : 'p_password_insert',
  S_PASSWORD_UPDATE : 'p_password_update',

  S_ROLE_INSERT : 'p_role_insert',
  S_ROLE_UPDATE : 'p_role_update',

  S_RESPONSE_CONTAINER : 'p_response_container',
  S_RESPONSE : 'p_response',
};
