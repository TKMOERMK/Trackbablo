ALTER TABLE "Расходы"
ADD COLUMN IF NOT EXISTS source_id VARCHAR(36);
CREATE UNIQUE INDEX IF NOT EXISTS ux_expenses_source_id
ON "Расходы" (source_id);
