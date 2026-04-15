# EchoNT Object-Oriented Class Diagram

This diagram outlines the Object-Oriented structure of our Django models, demonstrating encapsulation, class attributes, and business logic methods.

```mermaid
classDiagram
    class User {
        +int id
        +String username
        +String email
        +String password
    }

    class UserProfile {
        +int id
        +String bio
        +User user
        +__str__() String
    }

    class Species {
        +int id
        +String name
        +String scientific_name
        +List~Habitat~ habitats
        +__str__() String
    }

    class Habitat {
        +int id
        +String name
        +__str__() String
    }

    class Observation {
        +int id
        +DateTime date_spotted
        +String notes
        +User user
        +Species species
        +is_recent() bool
        +__str__() String
    }

    %% Relationships
    User "1" -- "1" UserProfile : OneToOne
    User "1" -- "*" Observation : ForeignKey (OneToMany)
    Species "1" -- "*" Observation : ForeignKey (OneToMany)
    Species "*" -- "*" Habitat : ManyToMany