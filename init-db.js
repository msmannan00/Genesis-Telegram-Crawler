db = db.getSiblingDB('mongo_grading_system');
db.c_users.drop();

db.c_users.save(
  {
    m_username: 'admin',
    m_password: 'admin',
    m_role: 'admin'
  }
);