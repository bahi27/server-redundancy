-- ===== NOTE IMPORTANTE =====
-- Le slave NE DOIT PAS créer d'utilisateurs ou de bases
-- car elles arrivent du master via pg_basebackup
-- Cet utilisateur (replicator) est créé par master-init.sql
-- et copié automatiquement via la réplication

COMMIT;