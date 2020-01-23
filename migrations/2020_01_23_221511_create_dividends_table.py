from orator.migrations import Migration


class CreateDividendsTable(Migration):

  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create('dividends') as table:
      table.increments('id')
      table.timestamps()
      table.integer('date').nullable()
      table.date('formatted_date').nullable()
      table.integer('amount').nullable()
      table.integer('dividendable_id').unsigned()
      table.foreign('dividendable_id').references('id').on('dividendables')

  def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop('dividends')
