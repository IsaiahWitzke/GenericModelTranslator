
package workreport;
//
//  all your imports go here
//
@Repository
public class BankAccountRepository {
    @Autowired
    private NamedParameterJdbcTemplate db;
    public List[BankAccount] findAll() {
        return db.query("SELECT * FROM bank_account;",
                BeanPropertyRowMapper.newInstance(BankAccount.class));
    }
    public Long create(BankAccount bankAccount) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        String create = String.join(" ", "INSERT INTO bank_account",
                "(bank_account_id, user_id, account_value, )",
                "VALUES (:bankAccountId, :userId, :accountValue, )");
        db.update(create, new BeanPropertySqlParameterSource(bankAccount), keyHolder);
        return Long.valueOf(keyHolder.getKeys().get("bank_account_id").toString());
    }
    public int update(BankAccount bankAccount) {
        String query = String.join(" ", "UPDATE bank_account SET",
                "bank_account_id = :bankAccountId, user_id = :userId, account_value = :accountValue, ",
                "WHERE bank_account_id = :bankAccountId");
        return db.update(query, new BeanPropertySqlParameterSource(bankAccount));
    }
    public int delete(Long bankAccountId) {
        String query = "DELETE FROM bank_account WHERE bank_account_id = :bankAccountId";
        return db.update(query,
                new MapSqlParameterSource("bankAccountId", bankAccountId));
    }
}
