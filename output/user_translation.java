
    package workreport;
    //
    //  all your imports go here
    //
    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    @Entity
    class User {
        @Id
        private Long userId;
        @NonNull
        @Size(min = 0, max = 255)
        private String userFirstName;
        @NonNull
        @Size(min = 0, max = 255)
        private String userLastName;
        @Nullable
        @Size(min = 0, max = 255)
        private String userAddr;
        // TODO: add custom constructors here
    }
