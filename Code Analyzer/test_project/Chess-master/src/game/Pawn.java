package game;

import java.util.*;

public class Pawn extends Piece
{
    private boolean firstMove;

    public Pawn(char x, int y, boolean color, String name)
    {
        super(x, y, color, name);
        this.firstMove = true;
    }

    public void setFirstMove(boolean flag)
    {
        this.firstMove = flag;
    }

    public boolean getFirstMove()
    {
        return this.firstMove;
    }
    
    public boolean canMove(char x, int y)
    {
        if( this.x - x == 0 )
        {
            if( Math.abs(this.y - y) == 1 || (this.firstMove && Math.abs(this.y - y) == 2) )
            {
                if( (this.color && this.y - y > 0) || (!this.color && y - this.y > 0) )
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
        }
        else if( Math.abs(this.x - x) == 1 && Math.abs(this.y - y) == 1 )
        {
            return true;
        }
        return false;
    }

    @Override
    public boolean crossMove(char x, int y)
    {
        if( Math.abs(this.x - x) == 1 && Math.abs(this.y - y) == 1 )
        {
            return true;
        }
        return false;
    }

    public boolean checkWay(ArrayList<Piece> pieces, char x, int y)
    {
        if( Math.abs(this.x - x) == 1 && Math.abs(this.y - y) == 1 )
        {
            return true;
        }
        else if( Math.abs(this.y - y) == 1 )
        {
            return true;
        }
        else
        {
            int yShift = (y - this.y) / Math.abs(y - this.y);
            if( checkTaken(pieces, this.x, this.y + yShift) != null  || checkTaken(pieces, this.x, this.y + 2 * yShift) != null )
            {
                return false;
            }
            return true;
        }
    }
}