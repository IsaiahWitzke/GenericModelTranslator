
package workreport;
//
//  all your imports go here
//
@Data
@AllArgsConstructor
@NoArgsConstructor
@Entity
class BankAccount {
    @Id
    private Long bankAccountId;
    @NonNull
    private Long userId;
    @NonNull
    private int accountValue;
    // TODO: add custom constructors here
}
