import { type Assume, type Column, type DrizzleTypeError, type Equal, type Simplify, type Table } from 'drizzle-orm';
import { z } from 'zod';
declare const literalSchema: z.ZodUnion<[z.ZodString, z.ZodNumber, z.ZodBoolean, z.ZodNull]>;
type Literal = z.infer<typeof literalSchema>;
type Json = Literal | {
    [key: string]: Json;
} | Json[];
export declare const jsonSchema: z.ZodType<Json>;
type MapInsertColumnToZod<TColumn extends Column, TType extends z.ZodTypeAny> = TColumn['_']['notNull'] extends false ? z.ZodOptional<z.ZodNullable<TType>> : TColumn['_']['hasDefault'] extends true ? z.ZodOptional<TType> : TType;
type MapSelectColumnToZod<TColumn extends Column, TType extends z.ZodTypeAny> = TColumn['_']['notNull'] extends false ? z.ZodNullable<TType> : TType;
type MapColumnToZod<TColumn extends Column, TType extends z.ZodTypeAny, TMode extends 'insert' | 'select'> = TMode extends 'insert' ? MapInsertColumnToZod<TColumn, TType> : MapSelectColumnToZod<TColumn, TType>;
type MaybeOptional<TColumn extends Column, TType extends z.ZodTypeAny, TMode extends 'insert' | 'select', TNoOptional extends boolean> = TNoOptional extends true ? TType : MapColumnToZod<TColumn, TType, TMode>;
type GetZodType<TColumn extends Column> = TColumn['_']['dataType'] extends infer TDataType ? TDataType extends 'custom' ? z.ZodAny : TDataType extends 'json' ? z.ZodType<Json> : TColumn extends {
    enumValues: [string, ...string[]];
} ? Equal<TColumn['enumValues'], [string, ...string[]]> extends true ? z.ZodString : z.ZodEnum<TColumn['enumValues']> : TDataType extends 'array' ? z.ZodArray<GetZodType<Assume<TColumn['_'], {
    baseColumn: Column;
}>['baseColumn']>> : TDataType extends 'bigint' ? z.ZodBigInt : TDataType extends 'number' ? z.ZodNumber : TDataType extends 'string' ? z.ZodString : TDataType extends 'boolean' ? z.ZodBoolean : TDataType extends 'date' ? z.ZodDate : z.ZodAny : never;
type ValueOrUpdater<T, TUpdaterArg> = T | ((arg: TUpdaterArg) => T);
type UnwrapValueOrUpdater<T> = T extends ValueOrUpdater<infer U, any> ? U : never;
export type Refine<TTable extends Table, TMode extends 'select' | 'insert'> = {
    [K in keyof TTable['_']['columns']]?: ValueOrUpdater<z.ZodTypeAny, TMode extends 'select' ? BuildSelectSchema<TTable, {}, true> : BuildInsertSchema<TTable, {}, true>>;
};
export type BuildInsertSchema<TTable extends Table, TRefine extends Refine<TTable, 'insert'> | {}, TNoOptional extends boolean = false> = TTable['_']['columns'] extends infer TColumns extends Record<string, Column<any>> ? {
    [K in keyof TColumns & string]: MaybeOptional<TColumns[K], (K extends keyof TRefine ? Assume<UnwrapValueOrUpdater<TRefine[K]>, z.ZodTypeAny> : GetZodType<TColumns[K]>), 'insert', TNoOptional>;
} : never;
export type BuildSelectSchema<TTable extends Table, TRefine extends Refine<TTable, 'select'>, TNoOptional extends boolean = false> = Simplify<{
    [K in keyof TTable['_']['columns']]: MaybeOptional<TTable['_']['columns'][K], (K extends keyof TRefine ? Assume<UnwrapValueOrUpdater<TRefine[K]>, z.ZodTypeAny> : GetZodType<TTable['_']['columns'][K]>), 'select', TNoOptional>;
}>;
export declare function createInsertSchema<TTable extends Table, TRefine extends Refine<TTable, 'insert'> = Refine<TTable, 'insert'>>(table: TTable, 
/**
 * @param refine Refine schema fields
 */
refine?: {
    [K in keyof TRefine]: K extends keyof TTable['_']['columns'] ? TRefine[K] : DrizzleTypeError<`Column '${K & string}' does not exist in table '${TTable['_']['name']}'`>;
}): z.ZodObject<BuildInsertSchema<TTable, Equal<TRefine, Refine<TTable, 'insert'>> extends true ? {} : TRefine>>;
export declare function createSelectSchema<TTable extends Table, TRefine extends Refine<TTable, 'select'> = Refine<TTable, 'select'>>(table: TTable, 
/**
 * @param refine Refine schema fields
 */
refine?: {
    [K in keyof TRefine]: K extends keyof TTable['_']['columns'] ? TRefine[K] : DrizzleTypeError<`Column '${K & string}' does not exist in table '${TTable['_']['name']}'`>;
}): z.ZodObject<BuildSelectSchema<TTable, Equal<TRefine, Refine<TTable, 'select'>> extends true ? {} : TRefine>>;
export {};
