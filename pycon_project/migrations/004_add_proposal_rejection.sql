BEGIN;

ALTER TABLE "review_proposalresult" ADD COLUMN "rejection_reason" TEXT NOT NULL DEFAULT '';

COMMIT;