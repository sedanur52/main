### Objectif :

L'objectif principal de ce projet est de faciliter la saisie d'informations personnelles des patients à l'hôpital en utilisant la voix. Cela vise à améliorer l'expérience des patients, en particulier ceux qui peuvent avoir des difficultés à remplir des formulaires écrits en raison de problèmes de santé.

### Fonctionnalités principales :

# Interface de Connexion :
L'interface de connexion permet aux utilisateurs de se connecter à l'application à l'aide de leurs identifiants (nom d'utilisateur et mot de passe). Les utilisateurs sont authentifiés à partir d'une base de données PostgreSQL.

# Enregistrement d'Utilisateur :
 Les utilisateurs ont la possibilité de s'enregistrer s'ils ne possèdent pas de compte. Une fois enregistrés, ils peuvent se connecter à l'application.

# Saisie Vocale :
Lorsqu'un utilisateur est connecté, il peut utiliser la saisie vocale pour fournir des informations personnelles telles que le nom, le prénom, l'e-mail, l'âge, le numéro de téléphone, le consentement et le numéro de sécurité sociale. La saisie vocale est gérée par la bibliothèque speech_recognition.

# Validation des Données : 
Les données saisies vocalement sont validées pour s'assurer de leur exactitude. Par exemple, l'âge doit être un nombre entier, l'adresse e-mail doit être au format valide, etc.

# Enregistrement des Données : 
Une fois que les informations ont été saisies vocalement et validées, elles sont enregistrées dans une base de données PostgreSQL. Les informations incluent un identifiant unique, le nom, le prénom, l'e-mail, l'âge, le numéro de téléphone, le consentement et le numéro de sécurité sociale.

# Affichage des Informations :
Les informations enregistrées vont être affichées dans l'interface pour permettre aux utilisateurs de vérifier les données enregistrées.

# Gestion des Utilisateurs (Admin) : 
Les administrateurs ont la possibilité de visualiser toutes les informations enregistrées par les utilisateurs. Cela peut être utile pour le suivi des patients.
