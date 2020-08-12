
package workreport;
//
//  all your imports go here
//
@Repository
public class UserRepository {
    @Autowired
    private NamedParameterJdbcTemplate db;
    public List[User] findAll() {
        return db.query("SELECT * FROM user;",
                BeanPropertyRowMapper.newInstance(User.class));
    }
    public Long create(User user) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        String create = String.join(" ", "INSERT INTO user",
                "(user_id, user_first_name, user_last_name, user_addr, )",
                "VALUES (:userId, :userFirstName, :userLastName, :userAddr, )");
        db.update(create, new BeanPropertySqlParameterSource(user), keyHolder);
        return Long.valueOf(keyHolder.getKeys().get("user_id").toString());
    }
    public int update(User user) {
        String query = String.join(" ", "UPDATE user SET",
                "user_id = :userId, user_first_name = :userFirstName, user_last_name = :userLastName, user_addr = :userAddr, ",
                "WHERE user_id = :userId");
        return db.update(query, new BeanPropertySqlParameterSource(user));
    }
    public int delete(Long userId) {
        String query = "DELETE FROM user WHERE user_id = :userId";
        return db.update(query,
                new MapSqlParameterSource("userId", userId));
    }
}
