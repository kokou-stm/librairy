PGDMP                      |         	   bachelier    17.2    17.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    32768 	   bachelier    DATABASE     |   CREATE DATABASE bachelier WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE bachelier;
                     postgres    false            �            1259    32769    ecole    TABLE     s   CREATE TABLE public.ecole (
    nom_bachelier character varying(10),
    age_primary integer,
    genre boolean
);
    DROP TABLE public.ecole;
       public         heap r       postgres    false            �          0    32769    ecole 
   TABLE DATA           B   COPY public.ecole (nom_bachelier, age_primary, genre) FROM stdin;
    public               postgres    false    217   7       �      x������ � �     