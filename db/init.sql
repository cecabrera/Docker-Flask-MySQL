CREATE DATABASE employees;
use employees;

CREATE TABLE hired_employees (
    id int,
    name varchar(255),
    datetime varchar(255),
    department_id int,
    job_id int
);

CREATE TABLE departments (
    id int,
    department varchar(255)
);

CREATE TABLE jobs (
    id int,
    job varchar(255)
);
