BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 8125ce6a58d2

CREATE TABLE public.demo (
    id UUID DEFAULT gen_random_uuid() NOT NULL, 
    name VARCHAR(16) NOT NULL, 
    age INTEGER, 
    password VARCHAR(32), 
    gender INTEGER, 
    remark VARCHAR(256), 
    delete_reason VARCHAR(64), 
    is_deleted BOOLEAN DEFAULT false NOT NULL, 
    created_by_id UUID, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    created_by VARCHAR(64) NOT NULL, 
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
    updated_by_id UUID, 
    updated_by VARCHAR(32) NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

COMMENT ON COLUMN public.demo.id IS 'Primary Key';

COMMENT ON COLUMN public.demo.name IS 'Name, unique identifier';

COMMENT ON COLUMN public.demo.age IS 'Age';

COMMENT ON COLUMN public.demo.password IS 'Password';

COMMENT ON COLUMN public.demo.gender IS 'Refer to Gender enum';

COMMENT ON COLUMN public.demo.remark IS 'Remark';

COMMENT ON COLUMN public.demo.delete_reason IS 'Delete Reason';

COMMENT ON COLUMN public.demo.is_deleted IS 'Is Deleted(Logical Delete)';

COMMENT ON COLUMN public.demo.created_by_id IS 'Create User ID';

COMMENT ON COLUMN public.demo.created_at IS 'Create Date';

COMMENT ON COLUMN public.demo.created_by IS 'Create User Name';

COMMENT ON COLUMN public.demo.updated_at IS 'Update Date';

COMMENT ON COLUMN public.demo.updated_by_id IS 'Update User ID';

COMMENT ON COLUMN public.demo.updated_by IS 'Update User Name';

INSERT INTO alembic_version (version_num) VALUES ('8125ce6a58d2') RETURNING alembic_version.version_num;

COMMIT;

