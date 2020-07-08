
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
        @Size(min = 0, max = 255)
        private String accountHolderName;
        @Nullable
        @Size(min = 0, max = 255)
        private String accountHolderAddr;
        @NonNull
        private int accountValue;
        // TODO: add custom constructors here
    }
