from orator.migrations import Migration


class CreateDividendablesTable(Migration):

  def up(self):
    """
    Run the migrations.
    """
    with self.schema.create('dividendables') as table:
      table.increments('id')
      table.timestamps()
      table.char('symbol', 20)
      table.integer('next_dividend_date').nullable()
      table.string('next_dividend_formatted_date').nullable()
      table.boolean('next_dividend_actual').nullable()
      table.float('dividend_yield').nullable()
      table.float('volatililty').nullable()
      table.integer('average_volume').nullable()

  def down(self):
    """
    Revert the migrations.
    """
    self.schema.drop('dividendables')
