-- disable wallee payment provider
UPDATE payment_provider
   SET wallee_space_id = NULL,
       wallee_application_user_id = NULL,
       wallee_application_user_auth_key = NULL;
