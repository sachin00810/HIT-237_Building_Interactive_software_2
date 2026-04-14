classDiagram
    class User {
        +Integer id
        +String username
        +String email
        +String password
    }

    class UserProfile {
        +Integer id
        +Text bio
        +User user
    }

    class Species {
        +Integer id
        +String name
        +String scientific_name
        +List~Habitat~ habitats
    }

    class Habitat {
        +Integer id
        +String name
    }

    class Observation {
        +Integer id
        +DateTime date_spotted
        +Text notes
        +User user
        +Species species
        +is_recent() Boolean
    }

    User "1" -- "1" UserProfile : has
    User "1" -- "*" Observation : logs
    Species "1" -- "*" Observation : subject of
    Species "*" -- "*" Habitat : lives in
