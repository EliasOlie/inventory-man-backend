import psycopg2
from infrastructure.DB import DB

def create():
    try:
        DB.querie(
            """
            CREATE TABLE IF NOT EXISTS company (
                company_id uuid PRIMARY KEY UNIQUE,
                company_name varchar(70) UNIQUE,
                company_email varchar UNIQUE,
                company_cnpj varchar,
                company_address varchar,
                created_at DATE NOT NULL DEFAULT CURRENT_DATE,
                modified_at DATE NOT NULL DEFAULT CURRENT_DATE,
                email_verified boolean DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS iuser (
                user_id uuid PRIMARY KEY,
                user_name varchar(70),
                user_email varchar UNIQUE,
                user_company varchar(70) references company(company_name),
                user_role varchar DEFAULT 'Dono',
                user_password varchar,
                created_at DATE NOT NULL DEFAULT CURRENT_DATE,
                modified_at DATE NOT NULL DEFAULT CURRENT_DATE,
                is_active boolean DEFAULT TRUE,
                email_verified boolean DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS products (
                product_id uuid PRIMARY KEY UNIQUE,
                product_belongs varchar(70) REFERENCES company(company_name),
                product_name varchar(70),
                product_description varchar,
                product_price decimal(10,2),
                product_amount integer
            );
            CREATE TABLE IF NOT EXISTS producthist (
                product_id uuid,
                product_belongs varchar(70),
                product_name varchar(70),
                product_description varchar,
                product_price decimal(10,2),
                product_amount integer,
                created_at DATE NOT NULL DEFAULT CURRENT_DATE,
                modified_by varchar(70) NOT NULL,
                operation varchar(9) NOT NULL
            );
            """
        )
    except psycopg2.errors.DuplicateTable:
        DB.rb()
    print("Tabelas criadas")