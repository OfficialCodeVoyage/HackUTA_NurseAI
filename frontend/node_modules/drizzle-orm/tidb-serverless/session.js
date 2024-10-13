import { entityKind } from "../entity.js";
import { NoopLogger } from "../logger.js";
import {
  MySqlPreparedQuery,
  MySqlSession,
  MySqlTransaction
} from "../mysql-core/session.js";
import { fillPlaceholders, sql } from "../sql/sql.js";
import { mapResultRow } from "../utils.js";
const executeRawConfig = { fullResult: true };
const queryConfig = { arrayMode: true };
class TiDBServerlessPreparedQuery extends MySqlPreparedQuery {
  constructor(client, queryString, params, logger, fields, customResultMapper) {
    super();
    this.client = client;
    this.queryString = queryString;
    this.params = params;
    this.logger = logger;
    this.fields = fields;
    this.customResultMapper = customResultMapper;
  }
  static [entityKind] = "TiDBPreparedQuery";
  async execute(placeholderValues = {}) {
    const params = fillPlaceholders(this.params, placeholderValues);
    this.logger.logQuery(this.queryString, params);
    const { fields, client, queryString, joinsNotNullableMap, customResultMapper } = this;
    if (!fields && !customResultMapper) {
      return client.execute(queryString, params, executeRawConfig);
    }
    const rows = await client.execute(queryString, params, queryConfig);
    if (customResultMapper) {
      return customResultMapper(rows);
    }
    return rows.map((row) => mapResultRow(fields, row, joinsNotNullableMap));
  }
  iterator(_placeholderValues) {
    throw new Error("Streaming is not supported by the TiDB Cloud Serverless driver");
  }
}
class TiDBServerlessSession extends MySqlSession {
  constructor(baseClient, dialect, tx, schema, options = {}) {
    super(dialect);
    this.baseClient = baseClient;
    this.schema = schema;
    this.options = options;
    this.client = tx ?? baseClient;
    this.logger = options.logger ?? new NoopLogger();
  }
  static [entityKind] = "TiDBServerlessSession";
  logger;
  client;
  prepareQuery(query, fields, customResultMapper) {
    return new TiDBServerlessPreparedQuery(
      this.client,
      query.sql,
      query.params,
      this.logger,
      fields,
      customResultMapper
    );
  }
  all(query) {
    const querySql = this.dialect.sqlToQuery(query);
    this.logger.logQuery(querySql.sql, querySql.params);
    return this.client.execute(querySql.sql, querySql.params);
  }
  async transaction(transaction) {
    const nativeTx = await this.baseClient.begin();
    try {
      const session = new TiDBServerlessSession(this.baseClient, this.dialect, nativeTx, this.schema, this.options);
      const tx = new TiDBServerlessTransaction(
        this.dialect,
        session,
        this.schema
      );
      const result = await transaction(tx);
      await nativeTx.commit();
      return result;
    } catch (err) {
      await nativeTx.rollback();
      throw err;
    }
  }
}
class TiDBServerlessTransaction extends MySqlTransaction {
  static [entityKind] = "TiDBServerlessTransaction";
  constructor(dialect, session, schema, nestedIndex = 0) {
    super(dialect, session, schema, nestedIndex, "default");
  }
  async transaction(transaction) {
    const savepointName = `sp${this.nestedIndex + 1}`;
    const tx = new TiDBServerlessTransaction(
      this.dialect,
      this.session,
      this.schema,
      this.nestedIndex + 1
    );
    await tx.execute(sql.raw(`savepoint ${savepointName}`));
    try {
      const result = await transaction(tx);
      await tx.execute(sql.raw(`release savepoint ${savepointName}`));
      return result;
    } catch (err) {
      await tx.execute(sql.raw(`rollback to savepoint ${savepointName}`));
      throw err;
    }
  }
}
export {
  TiDBServerlessPreparedQuery,
  TiDBServerlessSession,
  TiDBServerlessTransaction
};
//# sourceMappingURL=session.js.map